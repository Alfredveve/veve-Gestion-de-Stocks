from django.contrib import admin
from . import models


class CategorysAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_name']


admin.site.register(models.Categorys, CategorysAdmin)


class VendorsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'adress', 'mobile', 'status', 'photo']


admin.site.register(models.Vendors, VendorsAdmin)


class UnitsAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_name']


admin.site.register(models.Units, UnitsAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'unit__title']
    list_display = ['title', 'detail', 'category', 'unit', 'photo']


admin.site.register(models.Products, ProductAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    search_fields = ['product__title']
    list_display = ['id', 'product', 'qty', 'price', 'total_amount', 'vendor', 'pur_date']


admin.site.register(models.Purchases, PurchaseAdmin)


class SalesAdmin(admin.ModelAdmin):
    search_fields = ['product__title']
    list_display = ['product', 'qty', 'price', 'total_amount', 'sale_date', 'customer_name', 'customer_adresse',
                    'customer_mobile', 'customer_email']


admin.site.register(models.Sales, SalesAdmin)


class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__unit__title']
    list_display = ['product', 'pur_qty', 'sale_qty', 'total_bal_qty', 'product_unit', 'pur_date', 'sale_date']


admin.site.register(models.Inventorys, InventoryAdmin)
