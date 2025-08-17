# passage
**Pipeline for Assessing Safety at Sea, Alerting, and Gathering Evidence**

This is an airflow pipeline that consolidates and ingest data on channel crossings.
It utilises Kafka queues to collect streaming data and airflow for batch processing.
Flask and plotly provides an API to visualise the information collected. 

# Setup

## Development environment

To run the application in development mode, you need to setup a python virtual environment and install the dependencies
Install python virtualenv using your package manager, for example `apt install python3-virtualenv`, then:

From the project's root directory
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`cp example.env .env` to setup out environemt.
You need to set an API key in order to run the AIS position reports API. 
Head to https://aisstream.io/ and get yourself an API Key then edit `.env` to set the `AIS_STREAM_API_KEY`.

You also need to run services such as Apache Kafka and Airflow. As well as postgres and redis.
In another terminal run `docker compose up`

You can use the kafka-ui by browsing to http://localhost:8080/ui/clusters/ais/all-topics


## Producers

These processes send events to a Kafka queues.

### AIS Producer
Inside a virtual environment run `python producers/ais_stream_producer.py`.
This will start sending AIS Position reports to a queue

## Consumers

### AIS Redis consumer
Stream incoming events from kafka ais updates queue into redis
`python consumers/ais_stream-redis-consumer.py`

