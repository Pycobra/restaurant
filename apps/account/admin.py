from django.contrib import admin

from .models import UserBase


@admin.register(UserBase)
class ProductAdmin(admin.ModelAdmin):
    pass


