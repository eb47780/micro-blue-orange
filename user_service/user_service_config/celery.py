import logging
import os

from celery import Celery, bootsteps
import kombu
from django.db import transaction


logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service_config.settings')

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
        name='queue-user',
        exchange='user',
        routing_key='user_service',
        channel=conn,
        durable=True
    )
    queue.declare()

    queue_payment_checkout = kombu.Queue(
        name='queue-payment-checkout',
        exchange='payment_checkout',
        routing_key='payment_checkout_service',
        channel=conn,
        durablae=True
    )
    queue_payment_checkout.declare()


class Consumer(bootsteps.ConsumerStep):
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
        from authcore.serializers import ClientSerializer, AddressSerializer
        from authcore.models import Customer, Address
        try:
            with transaction.atomic():
                customer = Customer.objects.filter(id=data['customer_id']).first()
                address = Address.objects.filter(id=data['address_id']).first()
                del data['customer_id']
                del data['address_id']
                data['customer'] = ClientSerializer(customer).data
                data['address'] = AddressSerializer(address).data 
                _publish(message=data, routing_key='paymentgateway_service', exchange='payment')
        except Exception as e:
            logging.exception(e)

        message.ack()

app.steps['consumer'].add(Consumer)
