from django.urls import path
from payment.views import stripe_webhook

urlpatterns = [
  path('api/webhook/', stripe_webhook, name='stripe-webhooks')
]