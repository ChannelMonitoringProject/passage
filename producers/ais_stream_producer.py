""" A producer for AIS Stream """
import os
import logging
import websocket
import json
from dotenv import load_dotenv
import rel
from kafka import KafkaProducer

load_dotenv()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())

API_KEY = os.environ.get("AIS_STREAM_API_KEY")
KAFKA_HOST = os.environ.get("KAFKA_HOST")
arena = json.loads(str(os.environ.get("AIS_STREAM_ARENA")))

producer = KafkaProducer(
    bootstrap_servers=KAFKA_HOST,
    api_version=(2, 2, 15),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def on_open(ws):
    logging.info("Subscribing to AIS Stream feed")
    subscribe_message = {
        "APIKey": API_KEY,
        "BoundingBoxes": arena,
        "FilterMessageTypes": [
            "PositionReport",
            "StandardSearchAndRescueAircraftReport",
        ],
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    logging.info(str(message) + "\n")
    data = json.loads(message)
    producer.send("ais.updates", data)


def on_error(ws, error):
    logging.error("Socket Error: ")
    pass


def on_close(ws, close_status_code, close_msg):
    logging.error("Closing Socket: ", close_status_code, " - ", close_msg)
    pass


def main():
    url = "wss://stream.aisstream.io/v0/stream"
    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    rel.signal(2, rel.abort)
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.dispatch()


if __name__ == "__main__":
    main()
