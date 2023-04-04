from django.db import models
from authcore.models import UserClient
from common.models import BaseCustomer, AutoCreateUpdateMixin
from payment.models import PaymentMethod
from autoslug import AutoSlugField
import uuid
import os


def product_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/product/', filename)


class Customer(BaseCustomer):
    user = models.OneToOneField(UserClient, on_delete=models.CASCADE, related_name='user_client')
    phone = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Customer'

    def __str__(self):
        return self.user.email


class Address(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_client_address')
    street = models.CharField(max_length=200)
    street_number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'

    def __str__(self) -> str:
        return self.customer.email + ': ' + self.street + ' ' + self.street_number + ', ' + self.city + ' ' + self.zipcode


class Category(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='name')
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    image = models.ImageField(max_length=255, upload_to=product_image_file_path)

    class Meta:
        verbose_name = 'product'

    def __str__(self) -> str:
        return self.title


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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user_client_checkout')
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name='payment_method')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, related_name='status')
    bank_slip_url = models.URLField(blank=True, null=True, verbose_name='billet_url')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='checkout_item_product')
    quantity = models.PositiveSmallIntegerField(verbose_name='quantity')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='price')

    class Meta:
        verbose_name = 'checkout item'

    def __str__(self):
        return f'Email {self.checkout.customer.email} Date {self.created_at}'
