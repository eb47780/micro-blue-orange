import stripe
from payment.models import StripeGateway
from core.models import Customer, Checkout
from config import settings


def process_payment(validated_data):
    obj = StripeGateway.objects.filter().first()
    secret_key = getattr(obj, 'secret_key')
    stripe.api_key = secret_key.strip()

    customer = Customer.objects.filter(id=validated_data['customer']).first()
    checkout = Checkout.objects.filter(id=validated_data['checkout_id']).first()

    return None
