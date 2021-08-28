from datetime import datetime
from typing import ValuesView
from django.contrib import admin
import datetime
from django.db.models import F
from .models import Brand, Category, Contact, Discount, SubCategory, Product, Customer, UserProfileInfo
# Register your models here.
def change_public_day(modeladmin,request,queryset):
    queryset.update(public_day=datetime.date.today())
change_public_day.short_description = 'Mark Selected Products public_day to Today'

def increase_1_quantity(modeladmin,request,queryset):
    queryset.update(viewed = F('remains_quanity') + 1)
increase_1_quantity.short_description = 'Increase Viewed Selected Products 1 Unit'

def increase_5_quantity(modeladmin,request,queryset):
    queryset.update(viewed = F('remains_quanity') + 5)
increase_5_quantity.short_description = 'Increase Viewed Selected Products 5 Unit'

def increase_10_quantity(modeladmin,request,queryset):
    queryset.update(viewed = F('remains_quanity') + 10)
increase_10_quantity.short_description = 'Increase Viewed Selected Products 10 Unit'

def increase_50_quantity(modeladmin,request,queryset):
    queryset.update(viewed = F('remains_quanity') + 50)
increase_50_quantity.short_description = 'Increase Viewed Selected Products 50 Unit'

def increase_100_quantity(modeladmin,request,queryset):
    queryset.update(viewed = F('remains_quanity') + 100)
increase_100_quantity.short_description = 'Increase Viewed Selected Products 100 Unit'




admin.site.register(Category)
admin.site.register(SubCategory)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('viewed','public_day',)
    list_display = ('name','price','remains_quanity','viewed','public_day',)
    list_filter= ('public_day','subcategory')
    search_fields = ('name',)
    actions = [change_public_day,increase_1_quantity,increase_5_quantity,increase_10_quantity,increase_50_quantity,increase_100_quantity]

admin.site.register(Customer)
admin.site.register(UserProfileInfo)
admin.site.register(Discount)
admin.site.register(Brand)
admin.site.register(Contact)

admin.site.site_header = 'SportStore Admin'
