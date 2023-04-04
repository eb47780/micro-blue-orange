import stripe
from payment.models import StripeGateway


def process_payment(validated_data):
    obj = StripeGateway.objects.filter().first()
    secret_key = getattr(obj, 'secret_key')
    stripe.api_key = secret_key.strip()

    return None
