from django.contrib import admin
from checkout import models


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CheckoutItem)
class CheckoutItemAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'get_date')

    def get_customer(self, obj):
        return obj.checkout.customer

    get_customer.short_description = 'client'

    def get_date(self, obj):
        return obj.created_at

    get_date.short_description = 'date'


class CheckoutInline(admin.TabularInline):
    model = models.CheckoutItem


@admin.register(models.Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('get_customer', 'status', 'get_total')
    inlines = (CheckoutInline, )

    def get_customer(self, obj):
        return obj.customer

    get_customer.short_description = 'client'

    def get_total(self, obj):
        return obj.total

    get_total.short_description = 'total'
