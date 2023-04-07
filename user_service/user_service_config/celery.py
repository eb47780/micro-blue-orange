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


with rabbitmq_conn() as conn:
    queue = kombu.Queue(
        name='queue-user',
        exchange='user',
        routing_key='user_service',
        channel=conn,
        durable=True
    )
    queue.declare()
    print(queue)


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
        from authcore.models import Customer, Address, UserCheckout
        try:
            with transaction.atomic():
                customer = Customer.objects.filter(id=data['customer_id']).first()
                address = Address.objects.filter(id=data['address_id']).first()
                UserCheckout.objects.create(
                    customer_id=customer.id,
                    customer=customer,
                    address_id=address.id,
                    address=address,
                    checkout_id=data['checkout_id'],
                    payment_method_id = data['payment_method_id']
                    )
                logging.info('Task was completed successfully')
        except Exception as e:
            logging.exception(e)

        message.ack()


app.steps['consumer'].add(Consumer)
