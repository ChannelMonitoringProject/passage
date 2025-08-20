""" Consumers events from kafka and update redis """
import os
import uuid
import logging
from kafka import KafkaConsumer
import json, redis
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
r = redis.Redis(host="localhost", port=6379, db=0)

MAX_POINTS = 5000
KAFKA_HOST = os.environ.get("KAFKA_HOST")
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_HOST,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
)


def generate_id(mmsi: int, boat_name: str) -> str:
    name = boat_name.strip().replace(" ", "_").lower()
    ret = f"{mmsi}:{name}:{uuid.uuid4()}"
    logging.info(f"ID {ret}")
    return ret


def store_record(record):
    payload = record.value
    meta = payload["MetaData"]
    mmsi = meta["MMSI"]
    boat_name = meta["ShipName"]
    entry_id = generate_id(mmsi, boat_name)
    r.json().set(entry_id, "$", payload)


def main():
    for msg in consumer:
        logging.info(msg)
        store_record(msg)
        # r.lpush("ais:latest", json.dumps(msg.value))
        r.ltrim("ais:latest", 0, MAX_POINTS)


if __name__ == "__main__":
    main()
