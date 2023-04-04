from django.shortcuts import render
from .models import *

# Create your views here.

def main(request):
    context = {}
    return render(request, 'i_mall/main.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'i_mall/store.html', context)


def cart(request):
    context = {}
    return render(request, 'i_mall/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'i_mall/checkout.html', context)