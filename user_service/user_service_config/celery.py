from celery import Celery, bootsteps
import kombu
from django.db import transaction
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service_config.settings')

app = Celery('user_service_app')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()

# CONSUMER

def rabbitmq_conn():
    return app.pool.acquire(block=True)

with rabbitmq_conn() as conn:
    queue = kombu.Queue(
        name='queue-checkout',
        exchange='checkout',
        routing_key='user_service',
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
        pass

app.steps['consumer'].add(CheckoutConsumer)
