from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='homepage'),
    path('store/', views.StoreView.as_view(), name='store'),
    path('smartphone/', views.SmartphoneView.as_view(), name='smartphone'),
    path('laptop/', views.LaptopView.as_view(), name='laptop'),
    path('phukien/', views.PhuKienView.as_view(), name='phukien'),
    path('store/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:id>/',views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:id>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-history/<int:pk>/', views.OrderHistoryDetailView.as_view(), name='order-history'),
    path('register/', views.register, name='user-register'),
    path('profile/', views.profile, name='user-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
]
