from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from administration.admin import admin_site

# Models
from authcore.models import User

# Register user and user_admin
class UserAdmin(DjangoUserAdmin):
    pass

admin_site.register(User, UserAdmin)
