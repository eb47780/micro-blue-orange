from django.contrib.admin import apps

class AdministrationConfig(apps.AdminConfig):
    name = 'administration'
    default_site = 'admin.admin.AdminSite'
