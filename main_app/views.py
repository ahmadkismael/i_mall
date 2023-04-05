from django.shortcuts import render
from django.http import JsonResponse #Link up HTTP json to backend to be able to use JS in frontend
from .models import * #Gets ALL models
from django.contrib.auth.models import User #USER AUTH

# Create your views here.

def home(request):
    return render(request, 'i_mall/home.html')

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'i_mall/store.html', context)


def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'i_mall/cart.html', context)

def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'i_mall/checkout.html', context)

#Function that requests from HTML Json response that checks if ITEM was ADDED or NOT
def updateItem(request):
    return(JsonResponse('Item was added Successfully', safe=False))

