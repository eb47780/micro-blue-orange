from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from core import models


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
