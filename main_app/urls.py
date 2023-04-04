from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name = "main"),
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout")
]