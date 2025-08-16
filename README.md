# passage
**Pipeline for Assessing Safety at Sea, Alerting, and Gathering Evidence**

This is an airflow pipeline that consolidates and ingest data on channel crossings.
It utilises Kafka queues to collect streaming data and airflow for batch processing.
Flask and plotly provides an API to visualise the information collected. 

# Deployment

## Docker

To start the application, use `docker compose up`.

