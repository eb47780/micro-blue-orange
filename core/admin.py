from administration.admin import admin_site
import models


admin_site.register(models.Customer)
admin_site.register(models.Address)
admin_site.register(models.Product)
admin_site.register(models.Category)
