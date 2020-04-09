from django.contrib import admin
from .models import Customer,Product,Comment,OrderDetail,Order,Category
from django.conf import settings
from django.core.mail import send_mail
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
# admin.site.register(Order)

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'ammount', 'order_status','ordered')
    inlines = [OrderDetailInline]

    fieldsets = (
        ('Payment Information', {
            'fields': ('customer', 'ammount', 'shipping_address', 'order_status', 'ordered' )
        }),
        # ('Items Information', {
        #     'fields': ('status', 'due_back','borrower')
        # }),
    )

    def save_model(self, request, obj, form, change):
        if(obj.order_status=='a'):
            subject = "Cảm ơn bạn đã đặt hàng trên trang của chúng tôi."
            content = "Đơn hàng được chấp nhận" + "\n"
            content = "Sản phẩm bao gồm: " + "\n"
            for orderdetail in order.orderdetail_set.all():
                content += str(orderdetail.quantity)+ " " + str(orderdetail.item) + " giá " + str(orderdetail.price) + "\n"
            content += "Tổng số tiền: " + str(order.ammount) + "\n"
            content += "Địa chỉ giao hàng: " + str(order.shipping_address) + "\n"
            from_email = settings.EMAIL_HOST_USER
            to_list = [obj.customer.email, settings.EMAIL_HOST_USER]
            send_mail(subject, content, from_email, to_list, fail_silently=True)
        elif (obj.order_status=='d'):
            subject = "Cảm ơn bạn đã đặt hàng trên trang của chúng tôi."
            content = "Đơn hàng đã bị từ chối" + "\n"
            content = "Sản phẩm bao gồm: " + "\n"
            for orderdetail in order.orderdetail_set.all():
                content += str(orderdetail.quantity)+ " " + str(orderdetail.item) + " giá " + str(orderdetail.price) + "\n"
            content += "Tổng số tiền: " + str(order.ammount) + "\n"
            content += "Địa chỉ giao hàng: " + str(order.shipping_address) + "\n"
            from_email = settings.EMAIL_HOST_USER
            to_list = [obj.customer.email, settings.EMAIL_HOST_USER]
            send_mail(subject, content, from_email, to_list, fail_silently=True)
        super().save_model(request, obj, form, change)

# admin.site.register(OrderDetail)
admin.site.register(Category)
admin.site.register(Comment)
