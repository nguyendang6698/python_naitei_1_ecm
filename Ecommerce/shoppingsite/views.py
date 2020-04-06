from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
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


@login_required(login_url='/shoppingsite/login/')
def add_to_cart(request, id):
    redirect_to = request.GET.get('next', '')   # Lay chuoi next tu url tren template
    product = get_object_or_404(Product, id=id)
    cost = product.price
    # order_item = OrderDetail.objects.create(item=product)
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderdetail_set.filter(item__id=product.id).exists():
            order_item = order.orderdetail_set.filter(item__id=product.id)[0]
            order_item.quantity += 1
            order_item.price += cost
            order.ammount += cost
            order_item.save()
            order.save()
            messages.info(request, f"Da them <strong>1</strong> chiec <strong>{product.name}</strong> nua vao gio hang.<p>Hien co <strong>{order_item.quantity}</strong> chiec trong gio hang.</p>")
        else:
            order_item = OrderDetail.objects.create(item=product,order=order, price=cost)
            # order_item.price = cost
            order.orderdetail_set.add(order_item)
            order.ammount += cost
            order.save()
            messages.info(request, f"1 chiec <strong>{product.name}</strong> da vao gio hang.")
    else:
        order = Order.objects.create(customer=request.user, shipping_address=request.user.address)
        order_item = OrderDetail.objects.create(item=product,order=order,price=cost)
        # order_item.price = cost
        order.orderdetail_set.add(order_item)
        order.ammount += cost
        order.save()
        messages.info(request, f"1 chiec <strong>{product.name}</strong> da vao gio hang.")
    return HttpResponseRedirect(redirect_to)

@login_required(login_url='/shoppingsite/login/')
def remove_from_cart(request, id):
    redirect_to = request.GET.get('next', '')   # Lay chuoi next tu url tren template
    product = get_object_or_404(Product, id=id)
    cost = product.price
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderdetail_set.filter(item__id=product.id).exists():
            order.ammount -= cost*order.orderdetail_set.filter(item__id=product.id)[0].quantity
            order.orderdetail_set.filter(item__id=product.id).delete()
            order.save()
            messages.info(request, f"<strong>{product.name}</strong> da bi xoa khoi gio hang.")
        else:
            messages.info(request, f"Ban khong co SP nay trong gio hang.")
            return HttpResponseRedirect(redirect_to)  
    else:
        messages.info(request, f"Ban khong co SP nay trong gio hang.")
        return HttpResponseRedirect(redirect_to)  
    return HttpResponseRedirect(redirect_to)  

@login_required(login_url='/shoppingsite/login/')
def remove_single_item_from_cart(request, id):
    redirect_to = request.GET.get('next', '')   # Lay chuoi next tu url tren template
    product = get_object_or_404(Product, id=id)
    cost = product.price
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderdetail_set.filter(item__id=product.id).exists():
            order_item = order.orderdetail_set.filter(item__id=product.id)[0]
            # order.orderdetail_set.delete(order_item)
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order.ammount -= cost
                order_item.price -=cost
                order.save()
                order_item.save()
                messages.info(request, "Da bot 1 item ra khoi gio")
            else:
                order.ammount -= cost*order.orderdetail_set.filter(item__id=product.id)[0].quantity
                order.orderdetail_set.filter(item__id=product.id).delete()
                order.save()
                messages.info(request, f"<strong>{product.name}</strong> da bi xoa khoi gio hang.")
            return HttpResponseRedirect(redirect_to)
        else:
            messages.info(request, "SP nay chua co trong gio cua ban.")
            return HttpResponseRedirect(redirect_to)
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(redirect_to)


class OrderSummaryView(LoginRequiredMixin, generic.View):
    login_url="/shoppingsite/login/"
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'shoppingsite/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"Ban chua co gio hang.",extra_tags='danger')
            return redirect("/")


class CheckoutView(LoginRequiredMixin, generic.View):
    login_url="/shoppingsite/login/"
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'shoppingsite/checkout.html', context)
        except ObjectDoesNotExist:
            messages.error(request,"Ban chua co gio hang.")
            return redirect("/")
