from administration.admin import admin_site
from .models import Customer, Address

admin_site.register(Customer)
admin_site.register(Address)
