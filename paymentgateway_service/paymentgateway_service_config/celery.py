import logging
import os

from celery import Celery, bootsteps
import kombu
from django.db import transaction

logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paymentgateway_service_config.settings')

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


with rabbitmq_conn() as conn:
    queue = kombu.Queue(
        name='queue-payment',
        exchange='payment',
        routing_key='paymentgateway_service',
        channel=conn,
        durable=True
    )
    queue.declare()


class PaymentMethodConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [
            kombu.Consumer(
                channel,
                queues=[queue],
                callbacks=[self.handle_message],
                accept=['json']
            )
        ]

    def handle_message(self, data, message):
        with transaction.atomic():
            pass

app.steps['consumer'].add(PaymentMethodConsumer)
