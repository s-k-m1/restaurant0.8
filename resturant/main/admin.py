from django.contrib import admin
from .models import Contact, Category, Momo

# Register your models here.

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "phone_number", "email", "message"]
    ordering = ["id"]
    search_fields = ["full_name", "email", "phone_number"]





@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["id"]
    search_fields = ["name"]



@admin.register(Momo)
class MomoModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name","marked_price", "discount_percent", "selling_price", "selling_price1"]
    ordering = ["id"]
    search_fields = ["name"]