from django.contrib import admin
from payment.models import PaymentGateway, PaymentMethod, PaymentMethodEnum, PaymentMethodConfig, PolymorphicModel, StripeGateway
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(PaymentMethodConfig)
class PaymentMethodConfig(admin.ModelAdmin):
    pass


@admin.register(StripeGateway)
class StripeGatewayAdmin(PolymorphicChildModelAdmin):
    base_model = PaymentGateway


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(PolymorphicParentModelAdmin):
    base_model = PaymentGateway
    child_models = (StripeGateway, )
