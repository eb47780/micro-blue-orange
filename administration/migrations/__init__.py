from django.utils import module_loading

def autodiscover():
   module_loading.autodiscover_modules('admininstration')

default_app_config = 'administration.apps.AdminConfig'