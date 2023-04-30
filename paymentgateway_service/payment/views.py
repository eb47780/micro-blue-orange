from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from paymentgateway_service_config import settings
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging


STRIPE_API_KEY = 'sk_test_51MQWBTHJ9GTHbZihDblfeNFToPV2rgYvzHiJ2GwuTJzrkROJ8nmkWcCYNapVagJlVsMm0WkUyFWPb0tZK7a0bDBp00QuS0Is2O'
stripe.api_key = STRIPE_API_KEY


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
    
    send_mail(
      subject=f'Purchase at Blue Orange',
      message= f'Thank you for making a purchase at Blue Orange. Here is/are the product/s you ordered {product} at address {address}',
      recipient_list=[customer_email],
      from_email="endritpb@gmail.com"
    )

  return HttpResponse(status=200)
