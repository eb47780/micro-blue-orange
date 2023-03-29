from django.db import models
from authcore.models import UserClient
from common.models import BaseCustomer, AutoCreateUpdateMixin
import uuid
    
# Create your models here.
class Customer(BaseCustomer):
    user = models.OneToOneField(UserClient, on_delete=models.CASCADE, related_name='user_client')
    phone = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'client'

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
        verbose_name = 'address'
        verbose_name_plural = 'address'

    def __str__(self) -> str:
        return self.street + ' ' + self.street_number + ', ' + self.city + ' ' + self.zipcode