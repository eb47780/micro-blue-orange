from administration.admin import admin_site
import core.models as models


admin_site.register(models.Customer)
admin_site.register(models.Address)
admin_site.register(models.Product)
admin_site.register(models.Category)
