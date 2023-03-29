from django.contrib.admin import apps

class AdminConfig(apps.AdminConfig):
    name = 'administration'
    default_site = 'admin.admin.AdminSite'
