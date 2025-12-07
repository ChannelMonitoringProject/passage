FROM python:3.13
RUN mkdir -p /srv/kafka_consumers/
WORKDIR /srv/kafka_consumers/
COPY consumers/ais_stream_redis_consumer.py .
COPY ../requirements.consumers.txt requirements.txt
RUN pip install -r requirements.txt

# This will be some entrypoint.sh
ENTRYPOINT python ais_stream_redis_consumer.py 
