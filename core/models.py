from django.db import models
from autoslug import AutoSlugField
import uuid
import os

# Models
from authcore.models import UserClient
from common.models import BaseCustomer, AutoCreateUpdateMixin

# Helper functions
def product_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/product/', filename)

# Customer model
class Customer(BaseCustomer):
    user = models.OneToOneField(UserClient, on_delete=models.CASCADE, related_name='user_client')
    phone = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Customer'

    def __str__(self):
        return self.user.email
    
# Address Model
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

# Category Model
class Category(AutoCreateUpdateMixin): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='name')
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

# Product Model
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