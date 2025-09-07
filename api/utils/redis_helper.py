import os
import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import redis.exceptions

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)
r = redis.Redis(decode_responses=True)


def create_index():
    schema = [
        TextField("$.name", as_name="name"),
        TagField("$.city", as_name="city"),
        NumericField("$.age", as_name="age"),
    ]

    indexCreated = r.ft("idx:users").create_index(
        schema, definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON)
    )


def get_ais_state():
    ret = []
    return ret
