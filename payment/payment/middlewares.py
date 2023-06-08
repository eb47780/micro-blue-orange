from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from django.contrib import messages
from payment.models import PaymentMethodConfig, PaymentGateway


class CheckPaymentMethodConfigMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if not PaymentMethodConfig.objects.count():
            add_once_message(request, messages.WARNING, 'Configure payment method settings')


class CheckPaymentGatewayDefaultMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if not PaymentGateway.objects.count():
            add_once_message(request, messages.WARNING, 'Configure default payment gateway')


def add_once_message(request, level, msg):
    if msg not in [m.message for m in messages.get_messages(request)]:
        messages.add_message(request, level, msg)
