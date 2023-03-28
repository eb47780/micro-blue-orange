from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from administration.admin import admin_site
from authcore.models import User

# Register your models here.
class UserAdmin(DjangoUserAdmin):
    pass

admin_site.register(User, UserAdmin)
