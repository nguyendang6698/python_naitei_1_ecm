import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from shoppingsite.models import Customer,Product,Comment,OrderDetail,Order,Category
from django.contrib.auth import get_user_model 
User = get_user_model()

class StoreViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/shoppingsite/store/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingsite/store.html')
        
    def test_pagination_is_16(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['product_list']) == 16)

    def test_lists_all_products(self):
        # Get second page and confirm it has (exactly) remaining 8 items
        response = self.client.get(reverse('store')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['product_list']) == 8)


class ProfileViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user = User.objects.create_user(username='testuser', password='abc123456')
        
        test_user.save()
        
        # Create products
        Category.objects.create(name='Dien Thoai').save()
        number_of_products = 24

        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'iphone {product_id}',
                price= product_id*100,
                sku = 100,
                description= 'abc',
                category=Category.objects.get(pk=1)
            )
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('user-profile'))
        self.assertRedirects(response, '/shoppingsite/login/?next=/shoppingsite/profile/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='abc123456')
        response = self.client.get(reverse('user-profile'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'user/profile.html')


class CheckoutViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user = User.objects.create_user(username='testuser', password='abc123456')
        
        test_user.save()
        
        # Create products
        Category.objects.create(name='Dien Thoai').save()
        number_of_products = 24

        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'iphone {product_id}',
                price= product_id*100,
                sku = 100,
                description= 'abc',
                category=Category.objects.get(pk=1)
            )
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, '/shoppingsite/login/?next=/shoppingsite/checkout/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='abc123456')
        response = self.client.get(reverse('checkout'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'shoppingsite/checkout.html')


class OrderSummaryViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user = User.objects.create_user(username='testuser', password='abc123456')
        test_user.save()
        # Create products
        Category.objects.create(name='Dien Thoai').save()
        number_of_products = 24

        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'iphone {product_id}',
                price= product_id*100,
                sku = 100,
                description= 'abc',
                category=Category.objects.get(pk=1)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('order-summary'))
        self.assertRedirects(response, '/shoppingsite/login/?next=/shoppingsite/order-summary/')


class OrderHistoryViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user = User.objects.create_user(username='testuser', password='abc123456')
        
        test_user.save()
        
        # Create products
        Category.objects.create(name='Dien Thoai').save()
        number_of_products = 24

        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'iphone {product_id}',
                price= product_id*100,
                sku = 100,
                description= 'abc',
                category=Category.objects.get(pk=1)
            )
        
        self.order = test_user.order_set.create(ammount=10000, shipping_address="263 oik", ordered=True)
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('order-history',kwargs={'pk':self.order.pk}))
        self.assertRedirects(response, f'/shoppingsite/login/?next=/shoppingsite/order-history/{self.order.pk}/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='abc123456')
        response = self.client.get(reverse('order-history',kwargs={'pk':self.order.pk}))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'shoppingsite/order-detail.html')
