import logging
import os

from celery import Celery


logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS MODULE', 'checkout_service_config.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


def rabbitmq_conn():
    return app.pool.acquire(block=True)


def rabbitmq_producer():
    return app.producer_pool.acquire(block=True)


def _publish(message, routing_key):
    with rabbitmq_producer() as producer:
        producer.publish(
            body=message,
            routing_key=routing_key,
            exchange='checkout'
        )
