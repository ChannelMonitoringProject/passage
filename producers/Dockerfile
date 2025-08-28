FROM python:3
RUN mkdir -p /srv/kafka_producers/
WORKDIR /srv/kafka_producers/
COPY ./producers/ais_stream_producer.py .
COPY ../requirements.producers.txt requirements.txt
RUN pip install -r requirements.txt
# This will be some entrypoint.sh
ENTRYPOINT python ais_stream_producer.py 
