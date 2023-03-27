
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
