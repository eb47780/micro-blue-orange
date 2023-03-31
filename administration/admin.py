from django.contrib.admin import *
from django.contrib.auth.forms import AuthenticationForm

# Models
from core.models import *

# Create Admin Site
class AdminSite(AdminSite):
    site_header = 'Admin Owner'
    site_title = 'Admin Owner'
    index_title = 'Welcome Admin Owner'
    login_form = AuthenticationForm

admin_site = AdminSite(name='admin_site')