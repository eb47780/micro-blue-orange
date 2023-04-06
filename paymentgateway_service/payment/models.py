from django.db import models
from polymorphic.models import PolymorphicModel
from common.models import AutoCreateUpdateMixin
from enum import Enum
import uuid


class PaymentMethodEnum(Enum):
    CREDIT_CARD = 'credit_card'

payment_method_choices = [(pm.value, pm.name) for pm in PaymentMethodEnum]

class PaymentMethod(AutoCreateUpdateMixin):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'credit_card'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES, verbose_name='name')

    class Meta:
        verbose_name = 'payment method'

    def __str__(self):
        return self.get_name_display()
    

class PaymentMethodConfig(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name='payment method config')
    discount = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='discount', help_text='Discount in % (if not, leave it at 0)')

    class Meta:
        verbose_name = 'Configuration of payment methods'
        verbose_name_plural = 'Configuration of payment methods'

    def __str__(self) -> str:
        return self.payment_method.get_name_display()
    

class PaymentGateway(AutoCreateUpdateMixin, PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='name')
    default = models.BooleanField(default=False, verbose_name='main')


class StripeGateway(PaymentGateway):
    api_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'stripe.com'
        verbose_name_plural = 'stripe.com'
