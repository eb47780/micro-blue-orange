from django.db import models
import uuid


class AutoCreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseCustomer(AutoCreateUpdateMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, verbose_name='name')
    email = models.CharField(max_length=255, verbose_name='mail')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
