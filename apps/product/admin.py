from django.contrib import admin

from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import (Category, Product, ProductType) #, ProductImages)
admin.site.register(Category, MPTTModelAdmin)

    
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    pass

"""    
class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1
"""
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

"""
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):    
    inlines = [
        ProductImageInline,
    ]
    list_display = ['title',]
    list_filter = ['title', 'created_at']
    prepopulated_fields = {'slug':('title',)}
"""

