from django.db import models
from common.models import AutoCreateUpdateMixin
import uuid


class Status(AutoCreateUpdateMixin):
    STATUS = (
        ('Processing Purchase', 'Processing Purchase'),
        ('Approved Purchase', 'Approved Purchase'),
        ('Purchase Denied', 'Purchase Denied'),
        ('Purchase Sent', 'Purchase Sent')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=30, choices=STATUS)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'status'

    def __str__(self):
        return self.message


class Checkout(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.UUIDField(primary_key=False)
    address = models.UUIDField(primary_key=False)
    payment_method = models.UUIDField(primary_key=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, related_name='status')
    remote_id = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='remote_invoice_id', help_text='remote invoice id at the payment gateway')

    class Meta:
        verbose_name = 'checkout'

    @property
    def total(self):
        sum = 0
        for item in self.checkout_items.all():
            sum += item.price * item.quantity
        return sum


class CheckoutItem(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='checkout_items')
    product = models.UUIDField(primary_key=False)
    quantity = models.PositiveSmallIntegerField(verbose_name='quantity')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='price')

    class Meta:
        verbose_name = 'checkout item'

    def __str__(self):
        return f'Email {self.checkout.customer} Date {self.created_at}'
