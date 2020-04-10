import datetime

from django.test import TestCase
from django.utils import timezone

from shoppingsite.forms import CheckoutForm, CommentForm, SignupForm

class CheckoutFormTest(TestCase):
    def test_checkout_form_date_field_label(self):
        form = CheckoutForm()
        self.assertTrue(form.fields['address'].label == None or form.fields['address'].label == 'Address')
        
    def test_address_form_valid(self):
        form = CheckoutForm(data={'address': '123 abc, q.abc, p.abc, tp.abc'})
        self.assertTrue(form.is_valid())

class SignupFormTest(TestCase):

    def test_signup_form_email_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['username'].label == None or form.fields['username'].label == 'Username')
    
    def test_signup_form_first_name_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'First name')
    
    def test_signup_form_last_name_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'Last name')
    
    def test_signup_form_address_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['address'].label == None or form.fields['address'].label == 'Address')
    
    def test_signup_form_country_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['country'].label == None or form.fields['country'].label == 'Country')
    
    def test_signup_form_phone_field_label(self):
        form = SignupForm()
        self.assertTrue(form.fields['phone'].label == None or form.fields['phone'].label == 'Phone')

class CommentFormTest(TestCase):

    def test_comment_form_content_field_label(self):
        form = CommentForm()
        self.assertTrue(form.fields['content'].label == None or form.fields['content'].label == 'Content')
    
    def test_comment_form_content_field_valid(self):
        form = CommentForm()
        self.assertTrue(form.fields['content'].label == None or form.fields['content'].label == 'Content')

    def test_comment_form_content_valid(self):
        form = CommentForm(data={'content': 'abc123!@#$%^&*()_+-=~`'})
        self.assertTrue(form.is_valid())
