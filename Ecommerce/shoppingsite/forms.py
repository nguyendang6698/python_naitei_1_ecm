from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','address','country','phone']


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(), required=False)


class CommentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        self.rating = kwargs.pop('rating', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.product = self.product
        comment.rating = self.rating
        comment.save()
    
    class Meta:
        model = Comment
        fields = ["content"]
