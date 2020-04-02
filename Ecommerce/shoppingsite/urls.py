from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('store', views.StoreView.as_view(), name='store'),
    path('store/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:id>/',views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>', views.remove_from_cart, name='remove-from-cart'),
    path('register/', views.register, name='user-register'),
    path('profile/', views.profile, name='user-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
]
