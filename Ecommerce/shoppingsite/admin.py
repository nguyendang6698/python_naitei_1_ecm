from django.contrib import admin
from .models import Customer,Product,Comment,OrderDetail,Order,Category
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
# admin.site.register(Order)

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'ammount', 'order_status')
    inlines = [OrderDetailInline]

    fieldsets = (
        ('Payment Information', {
            'fields': ('customer', 'ammount', 'shipping_address', 'order_status', 'ordered' )
        }),
        # ('Items Information', {
        #     'fields': ('status', 'due_back','borrower')
        # }),
    )

# admin.site.register(OrderDetail)
admin.site.register(Category)
