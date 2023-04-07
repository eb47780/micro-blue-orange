from django.db import models
from django.contrib.auth.models import AbstractUser
from authcore.managers import UserClientManager
from common.models import BaseCustomer, AutoCreateUpdateMixin
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User Authentication'


class UserClient(User):
    objects = UserClientManager()

    class Meta:
        proxy = True
        verbose_name = 'User Client'


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


class UserCheckout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer_checkout')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='customer_address')
    checkout_id = models.UUIDField(primary_key=False, null=False, editable=False)
    payment_method_id = models.UUIDField(primary_key=False, null=False, editable=False)
    status_id = models.UUIDField(primary_key=False, null=False, editable=True)

    class Meta:
        verbose_name = 'User Checkout'

    def __str__(self) -> str:
        return self.customer.email + ', ' + self.checkout_id
