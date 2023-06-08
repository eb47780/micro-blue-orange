from payment.models import PaymentMethod
from payment.serializers import PaymentMethodSerializer
from config import settings
import stripe
import logging


stripe.api_key = settings.STRIPE_API_KEY
DOMAIN = 'http://localhost:4200'


def create_invoice(customer, amount):
    invoice = stripe.Invoice.create(customer=customer['id'])
    stripe.InvoiceItem.create(
        customer=customer['id'],
        amount=amount,
        invoice=invoice.id,
    )
    finalized_invoice = stripe.Invoice.pay(invoice['id'])
    return finalized_invoice


def checkout_session(data):
    checkout = data['checkout']
    payment_method = PaymentMethodSerializer(PaymentMethod.objects.filter(id=data['payment_method_id']).first()).data
    address = {
        'city': data['address']['city'],
        'line1': data['address']['street'] + ' ' + data['address']['street_number'],
        'postal_code': data['address']['zipcode']
    }
    metadata = {}
    metadata['customer'] = data['customer']['email']
    metadata['address'] = data['address']['street'] + ' ' + data['address']['street_number'] + ', ' + data['address']['city']

    line_items = []
    for item in checkout['items']:
        data_passed = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(float(item['price']))*100,
                'product_data': {
                    'name': item['title'],
                },
            },
            'quantity': int(item['quantity'])
        }
        metadata['product'] = item['title']
        line_items.append(data_passed)

    stripe.checkout.Session.create(
        payment_method_types=[payment_method['name']],
        line_items=line_items,
        mode='payment',
        success_url=DOMAIN + '/success',
        cancel_url=DOMAIN + '/failed',
        metadata=metadata
    )

    customer = stripe.Customer.list(
        email=data['customer']['email']
    )

    if len(customer['data']) != 0:
        customer = stripe.Customer.retrieve(id=customer['data'][0]['id'])
    else:
        customer = stripe.Customer.create(
            email=data['customer']['email'],
            name=data['customer']['name'],
            phone=data['customer']['phone'],
            address=address
        )

    card = stripe.Customer.create_source(customer['id'], source='tok_visa')
    intent = stripe.PaymentIntent.create(
        amount=int(float(data['checkout']['total']))*100,
        currency='usd',
        customer=customer['id'],
        payment_method=card['id']
    )
    stripe.PaymentIntent.confirm(intent['id'], payment_method=card['id'])
    finalized_invoice = create_invoice(customer, int(float(data['checkout']['total']))*100)

    return finalized_invoice.hosted_invoice_url
