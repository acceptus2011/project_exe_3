from django.contrib import admin

from myapp.models import Product, Purchase, Return

# Register your models here.
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)
