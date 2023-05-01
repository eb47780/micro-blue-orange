from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from paymentgateway_service_config import settings
import stripe
import logging


stripe.api_key = settings.STRIPE_API_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logging.exception(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logging.exception(e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
          event['data']['object']['id'],
          expand=['line_items'],
        )

        customer_email = session['metadata']['customer']
        product = session['metadata']['product']
        address = session['metadata']['address']

        msg = EmailMessage(
          f'Thank you for making a purchase at Blue Orange. Here is/are the product/s you ordered {product} at address {address}',
          subject='Purchase at Blue Orange',
          to=[customer_email]
        )
        msg.send()
    
    return HttpResponse(status=200)
