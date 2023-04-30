from payment.models import PaymentMethod
from payment.serializers import PaymentMethodSerializer
import logging
import stripe

#for now
STRIPE_API_KEY = 'sk_test_51MQWBTHJ9GTHbZihDblfeNFToPV2rgYvzHiJ2GwuTJzrkROJ8nmkWcCYNapVagJlVsMm0WkUyFWPb0tZK7a0bDBp00QuS0Is2O'
stripe.api_key = STRIPE_API_KEY

DOMAIN = 'http://localhost:4200'

def checkout_session(data):
    checkout = data['checkout']
    customer = data['customer']
    address = data['address']
    payment_method = PaymentMethodSerializer(PaymentMethod.objects.filter(id=data['payment_method_id']).first()).data
    
    line_items = []
    for item in checkout['items']:
        logging.warning(item)
        data_passed = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(float(item['price'])),
                'product_data': {
                    'name': item['title'],
                    # 'images': [item['image']]
                },
            },
            'quantity': int(item['quantity'])
        }
        line_items.append(data_passed)
        
    session = stripe.checkout.Session.create(
        payment_method_types = [payment_method['name']],
        line_items = line_items,
        mode='payment',
        success_url=DOMAIN+'/success',
        cancel_url=DOMAIN+'/failed'
    )    
    return session.id
