import logging
import os
import time

from celery import Celery, bootsteps
import kombu

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

''' setting publisher '''
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

class PaymentConsumer(bootsteps.ConsumerStep):
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
        from rest_framework_simplejwt.models import TokenUser
        token = TokenUser.objects.filter(token=data['requested_token'])
        print(token)
        if token.exists() and token.values()[0]['status'] == 'valid':
            pass
        import time
        time.sleep(5)
        print(data, message)
        message.ack()
    

app.steps['consumer'].add(PaymentConsumer)
