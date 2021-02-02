from django.contrib import admin

from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'available']
    list_editable = ['available']
admin.site.register(Product, ProductAdmin)


