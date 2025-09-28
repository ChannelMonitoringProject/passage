# passage
**Pipeline for Assessing Safety at Sea, Alerting, and Gathering Evidence**

This is an airflow pipeline that consolidates and ingest data on channel crossings from multiple sources.
It  will collect positioning, search and rescue and weather data for alerting and future analysis.


## Overview
This utilises Kafka queues to collect streaming data.
It will use Airflow for Batch processing.
It uses Redis for streaming data and it will use Postgres for storage.
Flask and plotly will provide an API to visualise the information collected. 

# Setup
## Docker

### Development docker setup
The docker environment is defined in `./infra/dev`. You will need to configure a few environment variables in a .env file

`cd infra/dev; cp example.env .env` to setup out environemt.

You need to set an API key in order to run the AIS position reports API. 
Head to https://aisstream.io/ and get yourself an API Key then edit `.env` file to set the `AIS_STREAM_API_KEY` to match your API key.

then run `docker compose up`

### Staging
Not implemneted yet 

### Production
Not implemneted yet 

## Development environment

To run the application in development mode, you need to setup a python virtual environment and install the dependencies
Install python virtualenv using your package manager, for example `apt install python3-virtualenv`, then:

From the project's root directory
```bash
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
You can use the kafka-ui by browsing to http://localhost:8080/ui/clusters/ais/all-topics

you can run the flask appliction by running 
`flask --app api`

## Producers

These processes send events to a Kafka queues.

### AIS Producer
Inside a virtual environment run `python producers/ais_stream_producer.py`.
This will start sending AIS Position reports to a queue

## Consumers

### AIS Redis consumer
Stream incoming events from kafka ais updates queue into redis
`python consumers/ais_stream_redis_consumer.py`

