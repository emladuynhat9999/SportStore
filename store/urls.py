from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index.html'),
    path('cart', views.cart, name='cart.html'),
    path('account', views.account, name='account.html'),
    path('contact', views.contact, name='contact.html'),
    path('products_detail/<int:pk>/', views.products_detail, name='products_detail.html'),
    path('products/<int:pk>/', views.products, name='products.html'),
    path('login', views.log_in, name='login.html'),
    path('logout', views.log_out, name='logout.html'),
    path('signin', views.sign_in, name='signin.html'),
]
