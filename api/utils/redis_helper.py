import os
import logging

import redis
from redis.commands.search import Search
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField, GeoField

# from redis.commands.search.index_definition import IndexType
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from redis.commands.search.query import Query
import redis.exceptions
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)

REDIS_BOAT_POSITION_REPORT_INDEX = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_INDEX", "position_reports_index"
)

# r = redis.Redis(decode_responses=True)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def create_index():
    schema = [
        NumericField("$.MetaData.MMSI", as_name="mmsi"),
        TextField("$.MetaData.ShipName", as_name="name"),
        NumericField("$.MetaData.unix_time", as_name="timestamp"),
        GeoField("$.MetaData.position", as_name="position"),
    ]

    indexCreated = r.ft(REDIS_BOAT_POSITION_REPORT_INDEX).create_index(
        schema,
        definition=IndexDefinition(
            prefix=[f"{REDIS_BOAT_POSITION_REPORT_TOPIC}"], index_type=IndexType.JSON
        ),
    )


def create_index_if_missing():
    try:
        r.ft(REDIS_BOAT_POSITION_REPORT_INDEX).info()
    except redis.exceptions.ResponseError as rerr:
        logging.info(f"No index {REDIS_BOAT_POSITION_REPORT_INDEX} found, creating")
        create_index()


def get_positioning_averages(start_time, end_time):
    query = ""
    search = Search(r, index_name=REDIS_BOAT_POSITION_REPORT_INDEX)
    request = aggregations.AggregateRequest(query)


def get_ais_state(start: int = 0, end: int = 3154118400):
    q = f"@timestamp:[{start} {end}]"
    req = aggregations.AggregateRequest(q)
    req = req.load(*["__key", "@mmsi", "@name", "@timestamp", "position"])
    # req = req.group_by(["@mmsi", "@name"], reducers.max("timestamp").alias("last_seen"))
    req = req.group_by(
        ["@mmsi", "@name"],
        reducers.max("@timestamp").alias("ts"),
        reducers.first_value("@position").alias("pos"),
    )
    req = req.group_by(["@mmsi", "@name", "@ts"])
    res = r.ft(REDIS_BOAT_POSITION_REPORT_INDEX).aggregate(req).rows
    logging.debug("aggregated ais state to: ", res)
    return res
