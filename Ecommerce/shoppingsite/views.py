from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm, CheckoutForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Product, Customer, Order, OrderDetail, Comment, Category
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.core.mail import EmailMessage

User = get_user_model()
# from django.contrib.auth import login, authenticate

# Create your views here.

class IndexView(generic.View):
    
    def get(self, *args, **kwargs):
        try:
            categories = Category.objects.all()
            context = {
                'categories': categories,
            }
            return render(self.request, 'shoppingsite/index.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Khong co category.", extra_tags='danger')
            return render(self.request, 'shoppingsite/index.html')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data.get('username')
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Hãy kích hoạt tài khoản của bạn.'
            message = render_to_string('user/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = [form.cleaned_data.get('email'),]
            
            # email = EmailMessage(email_subject, message, to=[to_email])
            # email.send()

            from_email = settings.EMAIL_HOST_USER
            send_mail(email_subject, message, from_email, to_email, fail_silently=True)
            messages.success(request, f'Chào mừng {username}, chúng tôi đã gủi email xác thực cho bạn, hãy check mail và kích hoạt tài khoản của bạn!')
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'user/user_register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, f'Chào mừng {user.username}, bạn đã đăng kí thành công!')
        return redirect("user-login")
    else:
        messages.warning(request, f'Kích hoạt không thành công')
        return redirect("/")

@login_required(login_url='/shoppingsite/login/')
def profile(request):
    return render(request, 'user/profile.html')


class StoreView(generic.ListView):
    model = Product
    template_name = 'shoppingsite/store.html'
    paginate_by = 16


class SmartphoneView(generic.View):
    
    def get(self, *args, **kwargs):
        try:
            smartphones = Product.objects.filter(category__exact=Category.objects.get(name="Dien Thoai"))
            context = {
                'product_list': smartphones,
            }
            return render(self.request, 'shoppingsite/store.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Khong co san pham trong muc nay", extra_tags='danger')
            return render(self.request, 'shoppingsite/store.html')


class LaptopView(generic.View):
    
    def get(self, *args, **kwargs):
        try:
            laptops = Product.objects.filter(category__exact=Category.objects.get(name="Laptop"))
            context = {
                'product_list': laptops,
            }
            return render(self.request, 'shoppingsite/store.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Khong co san pham trong muc nay", extra_tags='danger')
            return render(self.request, 'shoppingsite/store.html')


class PhuKienView(generic.View):
    
    def get(self, *args, **kwargs):
        try:
            phukien = Product.objects.filter(category__exact=Category.objects.get(name="Phu Kien"))
            context = {
                'product_list': phukien,
            }
            return render(self.request, 'shoppingsite/store.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Khong co san pham trong muc nay", extra_tags='danger')
            return render(self.request, 'shoppingsite/store.html')


class SmartphoneView(generic.View):
    
    def get(self, *args, **kwargs):
        try:
            smartphones = Product.objects.filter(category__exact=Category.objects.get(name="Dien Thoai"))
            context = {
                'product_list': smartphones,
            }
            return render(self.request, 'shoppingsite/store.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Khong co san pham trong muc nay", extra_tags='danger')
            return render(self.request, 'shoppingsite/store.html')


class ProductDetailView(generic.View):

    def get(self, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['pk'])
            comments = product.comment_set.all()
            count = product.comment_set.count()
            if count==0:
                count+=1
            average_rating = 0
            for c in comments:
                average_rating += c.rating/count
            average_rating = round(average_rating,1)
            average_rating_int = int(round(average_rating,0))
            five_star = comments.filter(rating=5).count()
            five_star_percent = round(five_star/count,2)*100
            four_star = comments.filter(rating=4).count()
            four_star_percent = round(four_star/count,2)*100
            three_star = comments.filter(rating=3).count()
            three_star_percent = round(three_star/count,2)*100
            two_star = comments.filter(rating=2).count()
            two_star_percent = round(two_star/count,2)*100
            one_star = comments.filter(rating=1).count()
            one_star_percent = round(one_star/count,2)*100
            form = CommentForm()
            context = {
            'product': product,
            'form':form,
            'comments':comments,
            'average_rating': average_rating,
            'average_rating_int': average_rating_int,
            'five_star': five_star,
            'five_star_percent': five_star_percent,
            'four_star': four_star,
            'four_star_percent': four_star_percent,
            'three_star': three_star,
            'three_star_percent': three_star_percent,
            'two_star': two_star,
            'two_star_percent': two_star_percent,
            'one_star': one_star,
            'one_star_percent': one_star_percent,
            }
            return render(self.request, 'shoppingsite/product_detail.html',context)
        except ObjectDoesNotExist:
            return render(self.request, 'shoppingsite/product_detail.html')
    
    def post(self, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        if self.request.POST.get('rating'):
            rating = self.request.POST['rating']
        else:
            rating = 0
        form = CommentForm(self.request.POST, user = self.request.user, product = product, rating=rating)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.request.path)


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
            messages.info(request, f"Đã thêm <strong>1</<strong> {product.name}</strong> vào giỏ hàng.<p>Hiện có <strong>{order_item.quantity}</strong> trong giỏ hàng.</p>")
        else:
            order_item = OrderDetail.objects.create(item=product,order=order, price=cost)
            # order_item.price = cost
            order.orderdetail_set.add(order_item)
            order.ammount += cost
            order.save()
            messages.info(request, f"1 <strong>{product.name}</strong> đã vào giỏ hàng.")
    else:
        order = Order.objects.create(customer=request.user, shipping_address=request.user.address)
        order_item = OrderDetail.objects.create(item=product,order=order,price=cost)
        # order_item.price = cost
        order.orderdetail_set.add(order_item)
        order.ammount += cost
        order.save()
        messages.info(request, f"1 <strong>{product.name}</strong> đã vào giỏ hàng.")
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
            form = CheckoutForm()
            context = {
            'order': order,
            'form' : form
            }
            return render(self.request, 'shoppingsite/checkout.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Ban khong co gio hang nao")
            return render(self.request, 'shoppingsite/checkout.html')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or NONE)
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                if form.cleaned_data.get('address')=='':
                    pass
                else:
                    order.shipping_address = form.cleaned_data.get('address')
            order.ordered = True
            for item in order.orderdetail_set.all():
                item.item.sku -= item.quantity
                item.item.save()
            order.save()
            messages.success(self.request,"Bạn đã đặt hàng thành công.")
            subject = "Cảm ơn bạn đã đặt hàng trên trang của chúng tôi."
            content = "Sản phẩm bao gồm: " + "\n"
            for orderdetail in order.orderdetail_set.all():
                content += str(orderdetail.quantity)+ " " + str(orderdetail.item) + " giá " + str(orderdetail.price) + "\n"
            content += "Tổng số tiền: " + str(order.ammount) + "\n"
            content += "Địa chỉ giao hàng: " + str(order.shipping_address) + "\n"
            from_email = settings.EMAIL_HOST_USER
            to_list = [self.request.user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, content, from_email, to_list, fail_silently=True)
            return redirect('order-history', pk=order.id)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Ban khong co gio hang nao")
            return render(self.request, 'shoppingsite/checkout.html')

class OrderHistoryDetailView(LoginRequiredMixin, generic.DetailView):
    login_url="/shoppingsite/login/"
    model = Order
    template_name = "shoppingsite/order-detail.html"

class SearchProductView(generic.View):

    def get(self, *args, **kwargs):
        try:
            category = self.request.GET.get('category')
            name = self.request.GET.get('product')
            if category == '0':
                product_list = Product.objects.filter(name__icontains=name)
            else:
                product_list = Product.objects.filter(category__id=category).filter(name__icontains=name)
            if product_list.count() != 0:
                pass
            else:
                messages.error(self.request, "Không có sản phẩm nào như vậy", extra_tags='danger')
            context = {
                    'product_list': product_list,
                }
            return render(self.request, 'shoppingsite/store.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Không có sản phẩm nào như vậy", extra_tags='danger')
            return render(self.request, 'shoppingsite/store.html')