# Create your tests here.

from django.test import TestCase
from shoppingsite.models import Customer,Product,Comment,OrderDetail,Order,Category
from django.contrib.auth import get_user_model 
User = get_user_model()

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Customer.objects.create(first_name='Den', last_name='Vau', username='denvau', address='NA', phone='NA', country='VN')

    def test_first_name_label(self):
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        customer= Customer.objects.get(id=1)
        field_label = customer._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'Last name')

    def test_first_name_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 30)

    def test_phone_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('phone').max_length
        self.assertEquals(max_length, 50)


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = Customer.objects.create(first_name='Den', last_name='Vau', username='denvau', address='NA', phone='NA', country='VN')
        number_of_products = 24
        Category.objects.create(name='Dien Thoai').save()

        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'iphone {product_id}',
                price= product_id*100,
                sku = 100,
                description= 'abc',
                category=Category.objects.get(pk=1)
            )
        order = test_user.order_set.create(ammount=10000, shipping_address="263 oik", ordered=True)
        orderdetail = OrderDetail.objects.create(order_id=1,item=Product.objects.get(pk=1), price=10000, sku=1, quantity=1)
        # order.orderdetail_set.add(orderdetail)

    def test_order_str_is_username_comma_date(self):
        order = Order.objects.get(id=1)
        expected_object_name = f'{order.customer.username}, {order.order_date.date()}'
        self.assertEquals(expected_object_name, str(order))

    def test_order_get_total_is_ammount(self):
        order = Order.objects.get(id=1)
        expected_object_value = order.ammount
        self.assertEquals(expected_object_value, order.ammount)
