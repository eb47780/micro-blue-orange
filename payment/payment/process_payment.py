from config import settings
import stripe


stripe.api_key = settings.STRIPE_API_KEY
DOMAIN = 'http://localhost:4200'


def create_invoice(customer, amount, card):
    invoice = stripe.Invoice.create(customer=customer['id'])
    stripe.InvoiceItem.create(
        customer=customer['id'],
        amount=amount,
        invoice=invoice.id,
        description=f"Invoice Payment for {customer['name']}"
    )
    finalized_invoice = stripe.Invoice.pay(invoice['id'], source=card)
    return finalized_invoice


def checkout_session(data):
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
    else:
        customer = stripe.Customer.create(
            email=data['customer']['email'],
            name=data['customer']['name'],
            phone=data['customer']['phone'],
            address=address
        )

    card = stripe.Customer.create_source(customer['id'], source='tok_visa')
    finalized_invoice = create_invoice(customer, int(float(data['checkout']['total']))*100, card)

    return finalized_invoice.hosted_invoice_url
