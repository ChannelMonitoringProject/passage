import os
import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import redis.exceptions
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 1))
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)
# r = redis.Redis(decode_responses=True)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def create_index():
    schema = [
        TextField("$.MetaData.MMSI", as_name="mmsi"),
        TextField("$.MetaData.ShipName", as_name="name"),
        TextField("$.MetaData.time_utc", as_name="time"),
    ]

    # indexCreated = r.ft("idx:users").create_index(
    indexCreated = r.ft("idx:boats").create_index(
        # indexCreated = r.ft(f"idx:{REDIS_BOAT_POSITION_REPORT_TOPIC}").create_index(
        schema,
        definition=IndexDefinition(
            prefix=[f"{REDIS_BOAT_POSITION_REPORT_TOPIC}"], index_type=IndexType.JSON
        ),
    )


def get_ais_state():
    req = aggregations.AggregateRequest("*").group_by(
        "@mmsi", reducers.count().alias("count")
    )

    # aggResult = r.ft("idx:boats").aggregate(req).rows
    aggResult = r.ft("idx:boats").aggregate(req).rows
    print(aggResult)

    query = Query("*")
    position_reports = (
        #        r.ft(f"idx:{REDIS_BOAT_POSITION_REPORT_TOPIC}").search(query).docs
        r.ft(f"idx:boats")
        .search(query)
        .docs
    )
    print(position_reports)
    for p in position_reports:
        print(p)
    return position_reports
    # ret = []
    # return ret
