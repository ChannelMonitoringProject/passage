from api.utils import redis_helper

import os
import redis
import redis.commands.search.aggregation as aggregations

from dotenv import load_dotenv

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)
# r = redis.Redis(decode_responses=True)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
load_dotenv()


def test_redis_query():
    assert False


def test_redis_ais_position_report_query():
    redis_helper.create_index_if_missing()
    state = redis_helper.get_ais_state()
    for s in state:
        print(s)
        assert set(["mmsi", "name", "ts", "pos"]).issubset(s.keys())


def test_create_position_reports_index():
    try:
        print("trying to drop the position_reports_index")
        r.ft("position_reports_index").dropindex(True)
    except redis.exceptions.ResponseError:
        print("No index")

    redis_helper.create_index()
    r.ft
    assert False


def test_drop_index():
    assert False
