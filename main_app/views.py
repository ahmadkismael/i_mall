from django.shortcuts import render
from django.http import JsonResponse #Link up HTTP json to backend to be able to use JS in frontend
import json #Grabbing data and parsing 
import datetime
from .models import * #Gets ALL models
from django.contrib.auth.models import User #USER AUTH

# Create your views here.

def home(request):
    return render(request, 'i_mall/home.html')

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
  
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'i_mall/store.html', context)


def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'i_mall/cart.html', context)
    
def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'i_mall/checkout.html', context)

#Function that requests from HTML Json response that checks if ITEM was ADDED or NOT
def updateItem(request):
    # Call json from front end to link to backend to load the requested data correctly 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
 
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':    
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return(JsonResponse('Item was added Successfully', safe=False))


def processOrder(request):
      transaction_id = datetime.datetime.now().timestamp()
      data = json.loads(request.body)

      if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                order.complete = True
            order.save()
            
            if order.shipping == True:
                ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
	)
      else:
            print('User is not logged in')
      return JsonResponse('Payment subbmitted..', safe=False)

