import pytest
from unittest.mock import Mock, patch
from consumers import ais_stream_redis_consumer
from consumers.ais_stream_redis_consumer import (
    generate_timestamp,
    store_record,
    generate_position,
)


def test_time_utc_string_to_unit_time():
    time_utc_str = "2025-09-28 20:34:39.010066909 +0000 UTC"
    unix_time_utc = generate_timestamp(time_utc_str)
    assert unix_time_utc == 1759084479


def test_generate_position():
    expected = "1.23 4.56"
    assert generate_position(1.23, 4.56) == expected


# @pytest.mark.skip(reason="Annoying to mock redis")
def test_store_record():
    redis_mock = Mock()
    json_mock = Mock()

    redis_mock.json.return_value = json_mock

    kafka_record_mock = Mock()

    # consumers.ais_stream_redis_consumer.r = redis_mock
    store_record.r = redis_mock

    record = {
        "Message": {
            "PositionReport": {},
        },
        "MetaData": {
            "MMSI": 69,
            "time_utc": "2025-09-28 20:34:39.010066909 +0000 UTC",
            "ShipName": "BOATY MACBOATFACE     ",
            "latitude": 51.33114,
            "longitude": 2.3744916666666667,
        },
    }

    kafka_record_mock.value = record

    expected_id = "ais.updates.boat_position_reports:69:boaty_macboatface:224fb8df-92c1-4ca9-b7e6-5141c9762905"
    store_record(kafka_record_mock)
    json_mock.assert_called()
