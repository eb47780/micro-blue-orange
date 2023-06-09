from config import settings
import stripe
from payment.models import PaymentMethod
from payment.serializers import PaymentMethodSerializer
import time


stripe.api_key = settings.STRIPE_API_KEY


def create_invoice(customer, items, payment_method):
    invoice = stripe.Invoice.create(customer=customer['id'])
    for description, unit_amount, quantity in zip(items['description'], items['unit_amount'], items['quantity']):
        stripe.InvoiceItem.create(
            customer=customer['id'],
            quantity=quantity,
            unit_amount=unit_amount,
            invoice=invoice.id,
            description=description
        )

    if payment_method == 'card':
        card = stripe.Customer.create_source(customer['id'], source='tok_visa')        
        finalized_invoice = stripe.Invoice.pay(invoice['id'], source=card)
        return finalized_invoice


def checkout_session(data):
    time.sleep(10)
    payment_method = PaymentMethodSerializer(PaymentMethod.objects.filter(id=data['payment_method_id']).first()).data
    
    items = {'description': [], 'unit_amount':[], 'quantity':[]}
    for item in  data['checkout']['items']:
        items['description'].append(item['title'])
        items['unit_amount'].append(int(float(item['price']))*100)
        items['quantity'].append(int(item['quantity']))
    
    address = {
        'city': data['address']['city'],
        'line1': data['address']['street'] + ' ' + data['address']['street_number'],
        'postal_code': data['address']['zipcode']
    }

    customer = stripe.Customer.list(
        email=data['customer']['email']
    )

    if len(customer['data']) != 0:
        customer = stripe.Customer.retrieve(id=customer['data'][0]['id'])
        customer = stripe.Customer.modify(
            sid=customer['id'],
            email=data['customer']['email'],
            name=data['customer']['name'],
            phone=data['customer']['phone'],
            address=address
        )
    else:
        customer = stripe.Customer.create(
            email=data['customer']['email'],
            name=data['customer']['name'],
            phone=data['customer']['phone'],
            address=address
        )

    finalized_invoice = create_invoice(customer, items, payment_method['name'])
    
    return finalized_invoice.hosted_invoice_url
