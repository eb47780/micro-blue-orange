import logging
import os

from celery import Celery, bootsteps
import kombu
from django.db import transaction

logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkout_service_config.settings')

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


def _publish(message, routing_key, exchange):
    with rabbitmq_producer() as producer:
        producer.publish(
            body=message,
            routing_key=routing_key,
            exchange=exchange
        )

with rabbitmq_conn() as conn:
    queue = kombu.Queue(
        name='queue-checkout',
        exchange='checkout',
        routing_key='checkout_service',
        channel=conn,
        durable=True
    )
    queue.declare()


class CheckoutConsumer(bootsteps.ConsumerStep):
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
        try:
            with transaction.atomic():
                from checkout.models import Checkout, Status
                checkout = Checkout.objects.filter(id=data['checkout_id']).first()
                status = Status.objects.filter(id=data['status_id']).first()
                checkout.status = status
                checkout.remote_id = data['remote_invoice_id']
                checkout.save()
                logger.info('Checkout Service Status Completed')
        except Exception as e:
            logger.exception(e)

        message.ack()


app.steps['consumer'].add(CheckoutConsumer)
