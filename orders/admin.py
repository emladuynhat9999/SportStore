from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
def change_paid(modeladmin,request,queryset):
    queryset.update(paid = True)
change_paid.short_description = 'Mark Selected Orders Paid to True'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email',
                    'address', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ('address',)
    actions = [change_paid]
    inlines = [OrderItemInline]
