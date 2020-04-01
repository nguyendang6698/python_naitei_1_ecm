from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Product, Customer, Order, OrderDetail, Comment, Category

# Create your views here.

def index(request):
    return render(request,'shoppingsite/index.html')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Chao mung {username}, ban la khach hang moi cua chung toi!')
            return redirect('user-login')
            # return HttpResponse("Thanh cong")
    else:
        form = SignupForm()
    return render(request, 'user/user_register.html', {'form': form})

@login_required(login_url='/shoppingsite/login/')
def profile(request):
    return render(request, 'user/profile.html')

class StoreView(generic.ListView):
    model = Product
    template_name = 'shoppingsite/store.html'
    paginate_by = 16

class ProductDetailView(generic.DetailView):
    model = Product
