from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter name for a category.')
    description = models.TextField(max_length=1000, help_text='Enter category description', default='')
    image = models.ImageField(default='category_default.png', upload_to='category_pics')
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, help_text='Enter name for a product.')
    price = models.IntegerField(default=0, blank=False)
    sku = models.IntegerField(default=0,blank=False)    # So luong hang trong kho
    description = models.TextField(max_length=1000, help_text='Enter product description', default='')
    image = models.ImageField(default='product_default.png', upload_to='product_pics')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', args=[str(self.id)])
    
    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', args=[str(self.id)])

class Customer(AbstractUser):
    address = models.CharField(max_length=500, help_text='Input your address.')
    country = models.CharField(max_length=500, help_text='Input your country.')
    phone = models.CharField(max_length=50, help_text='Enter your number', blank=False)
    image = models.ImageField(default='profile_default.png', upload_to='profile_pics')

class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    title = models.CharField(default='No title', max_length=500)
    rating = models.IntegerField(blank=True, null=True)
    content = models.TextField(default='', max_length=1000)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ammount = models.IntegerField(default = 0)      # Tong so tien
    shipping_address = models.CharField(max_length=500, help_text='Input address.')
    order_date = models.DateTimeField(auto_now_add=True)
    # ordered = models.BooleanField(default= False)
    
    STATUS = (
        ('a', 'accept'),
        ('p', 'pending'),
        ('d', 'decline'),
    )

    order_status = models.CharField(
        choices=STATUS,
        max_length=1,
        default='p',
        help_text='Order status',
        blank=True
    )

    def __str__(self):
        return f'{self.customer.username}, {self.order_date.date()}'

    def display_order_detail(self):
        return self.orderdetail_set.all()


class OrderDetail(models.Model):    # Chi tiet 1 item trong gio hang
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sku = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} {self.item.name}'
