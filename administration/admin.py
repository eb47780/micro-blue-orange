from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from core import models
from payment.models import PaymentMethod, PaymentGateway, StripeGateway, PaymentMethodConfig


class AdminSite(admin.AdminSite):
    site_header = 'Admin Owner'
    site_title = 'Admin Owner'
    index_title = 'Welcome Admin Owner'
    login_form = AuthenticationForm

admin_site = AdminSite(name='admin_site')


@admin.register(models.Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')
    search_fields = ('title', )

@admin.register(models.Customer, site=admin_site)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ['user']
    list_display = ('name', 'email')

@admin.register(models.Address, site=admin_site)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Status, site=admin_site)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(models.CheckoutItem, site=admin_site)
class CheckoutItemAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'get_date')

    def get_customer(self, obj):
        return obj.checkout.customer.email

    get_customer.short_description = 'client'

    def get_date(self, obj):
        return obj.created_at

    get_date.short_description = 'date'

class CheckoutInline(admin.TabularInline):
    model = models.CheckoutItem

@admin.register(models.Checkout, site=admin_site)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'payment_method', 'status', 'get_total')
    inlines = (CheckoutInline, )

    def get_customer(self, obj):
        return obj.customer.email

    get_customer.short_description = 'client'

    def get_total(self, obj):
        return obj.total

    get_total.short_description = 'total'


@admin.register(PaymentMethod, site=admin_site)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(PaymentMethodConfig, site=admin_site)
class PaymentMethodConfig(admin.ModelAdmin):
    pass

@admin.register(StripeGateway, site=admin_site)
class StripeGatewayAdmin(PolymorphicChildModelAdmin):
    base_model = PaymentGateway
    show_in_index = True

@admin.register(PaymentGateway, site=admin_site)
class PaymentGatewayAdmin(PolymorphicParentModelAdmin):
    base_model = PaymentGateway
    child_models = (StripeGateway, )
