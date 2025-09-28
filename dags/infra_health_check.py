from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import logging
import psycopg2
import redis
from kafka import KafkaConsumer


def check_postgres():
    try:
        conn = psycopg2.connect(
            dbname="airflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port=5432,
        )
        conn.close()
        logging.info("Postgres connection successful")
    except Exception as e:
        logging.error(f"Postgres connection failed: {e}")
        raise


def check_redis():
    try:
        r = redis.Redis(host="redis", port=6379)
        r.ping()
        logging.info("Redis connection successful")
    except Exception as e:
        logging.error(f"Redis connection failed: {e}")
        raise


def check_kafka():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers="kafka:9093",
            api_version_auto_timeout_ms=3000,
            request_timeout_ms=3000,
        )
        consumer.close()
        logging.info("Kafka connection successful")
    except Exception as e:
        logging.error(f"Kafka connection failed: {e}")
        raise


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}

dag = DAG(
    "infra_health_check",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    description="Simple DAG to check infra connectivity",
)

postgres_task = PythonOperator(
    task_id="check_postgres", python_callable=check_postgres, dag=dag
)

redis_task = PythonOperator(task_id="check_redis", python_callable=check_redis, dag=dag)

kafka_task = PythonOperator(task_id="check_kafka", python_callable=check_kafka, dag=dag)

postgres_task >> redis_task >> kafka_task
