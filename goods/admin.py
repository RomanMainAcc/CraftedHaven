from django.contrib import admin

from goods.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'discount', 'category', 'image')
    list_editable = ('price', 'discount')
    search_fields = ('name', 'description')
    list_filter = ('discount', 'category')
