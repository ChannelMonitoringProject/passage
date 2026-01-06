""" Consumers events from kafka and update redis """
import os
import datetime
import uuid
import logging
from kafka import KafkaConsumer
import json, redis
from dotenv import load_dotenv

load_dotenv()

if "REDIS_PASSWORD" not in os.environ:
    exit("Set environment variable REDIS_PASSWORD")

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())


KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost:9092")
MAX_POINTS = 5000
KAFKA_AIS_TOPIC = os.environ.get("KAFKA_AIS_TOPIC", "ais.updates")


REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)

r = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD
)

consumer = KafkaConsumer(
    KAFKA_AIS_TOPIC,
    bootstrap_servers=KAFKA_HOST,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
)


def generate_id(mmsi: int, boat_name: str) -> str:
    """Returns an id, "topic:mmsi:ship_name:uuid" """
    name = boat_name.strip().replace(" ", "_").lower()
    topic = REDIS_BOAT_POSITION_REPORT_TOPIC
    ret = f"{topic}:{mmsi}:{name}:{uuid.uuid4()}"
    logging.info(f"Redis record ID: {ret}")
    return ret


def generate_timestamp(time_utc: str) -> int:
    """Converts a datetime string to integer, drop microseconds"""
    time_utc = time_utc[0:19]
    unix_time = datetime.datetime.strptime(time_utc, "%Y-%m-%d %H:%M:%S").timestamp()
    return int(unix_time)


def generate_position(lat: float, lon: float):
    """Puts lat and lon in a way GeoRedis likes"""
    return f"{lat}, {lon}"


def store_record(record):
    payload = record.value
    if "PositionReport" in payload["Message"]:
        logging.info(
            f"Adding a position report to redis {REDIS_BOAT_POSITION_REPORT_TOPIC}"
        )
        meta = payload["MetaData"]
        mmsi = meta["MMSI"]
        boat_name = meta["ShipName"]
        entry_id = generate_id(mmsi, boat_name)

        # Add keys to help redis indexing
        time_utc = meta["time_utc"]
        payload["MetaData"]["unix_time"] = generate_timestamp(time_utc)
        payload["MetaData"]["position"] = generate_position(
            meta["latitude"], meta["longitude"]
        )
        r.json().set(entry_id, "$", payload)


def main():
    logging.info(f"Consuming {KAFKA_AIS_TOPIC} events from Kafka host {KAFKA_HOST}")
    logging.info(
        f"pushing {REDIS_BOAT_POSITION_REPORT_TOPIC} to Redis host {REDIS_HOST}:{REDIS_PORT}"
    )
    for msg in consumer:
        logging.debug(msg)
        store_record(msg)
        # r.lpush("ais:latest", json.dumps(msg.value))
        r.ltrim("ais:latest", 0, MAX_POINTS)


if __name__ == "__main__":
    main()
