""" Consumers events from kafka and update redis """
import os
import logging
from kafka import KafkaConsumer
import json, redis
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
r = redis.Redis(host="localhost", port=6379, db=0)

MAX_POINTS = 5000
KAFKA_HOST = os.environ.get("KAFKA_HOST")
TOPIC = "ais.updates"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_HOST,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
)


def main():
    for msg in consumer:
        logging.info(msg)
        r.lpush("ais:latest", json.dumps(msg.value))
        r.ltrim("ais:latest", 0, MAX_POINTS - 1)


if __name__ == "__main__":
    main()
