from celery import Celery, bootsteps
import kombu
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkout_service_config.settings')

app = Celery('checkout_service_app')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()

# PRODUCER

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
