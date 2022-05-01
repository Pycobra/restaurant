from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .cart import Cart
from .forms import CheckoutForm
from apps.product.models import Product


from apps.checkout.models import DeliveryOptions
from apps.order.models import Address


def shopping_cart(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

    else:
        form = CheckoutForm()
    return render(request, 'cart/cart.html', {'form':form})#, 'stripe_pub_key':settings.STRIPE_PUB_KEY})

@login_required
def cart_detail(request):
    cart = Cart(request)
    if request.POST.get('mainAction') == 'post':
        subAction = request.POST.get('subAction')
        productID = request.POST.get('productID')
        productQTY = 1
        if subAction == "delete":
            #item_quantity, item_total_cost, sub_total, total, delivery_price = cart.remove(product_id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.remove(product_id=str(productID))
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity,  'item_total_cost':item_total_cost,
                 'sub_total':sub_total, 'total':total, 'delivery_price':delivery_price})
            return response
        if subAction == 'add':
            product = get_object_or_404(Product, id=productID)
            product_exist = cart.add(product_id=productID, product=product, quantity=productQTY, update_quantity=False)
            response = JsonResponse(
                {'cart_length': cart.__len__()})
            return response

        if subAction == 'update':
            product = get_object_or_404(Product, id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.update(
                product_id=productID, product=product, quantity=productQTY, update_quantity=True)
            messages.success(request, 'The item was successfully updated in cart')
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity, 'item_total_cost': item_total_cost,
                 'sub_total': sub_total, 'total': total, 'delivery_price': delivery_price})
            return response

        if subAction == 'subtract':
            product = get_object_or_404(Product, id=productID)
            item_quantity, item_total_cost, sub_total, total, delivery_price = cart.subtract(product_id=productID, quantity=productQTY, update_quantity=True)
            messages.success(request, 'The account was successfully subtracted from account')
            response = JsonResponse(
                {'cart_length': cart.__len__(), "get_total_cost":cart.get_total_cost(),
                 'item_quantity': item_quantity, 'item_total_cost': item_total_cost,
                 'sub_total': sub_total, 'total': total, 'delivery_price': delivery_price})
            return response

@login_required
def inside_cart(request):
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        cart_1 = []
        all_id = []

        for i in cart:
            del i['product']
            all_id.append(i['id'])
            cart_1.append(i)
        products = Product.objects.filter(id__in=all_id)
        serialized2 = serializers.serialize('python', products)
        cart_items = {}
        cart_items['table'] = cart_1
        cart_items['product'] = serialized2
        for i in cart_items['table']:
            id = str(i['id'])
            for n in cart_items['product']:
                pk = str(n['pk'])
                if id == pk:
                    i['images'] = n['fields']['images']
                    i['title'] = n['fields']['title']
        total_qty = 0
        total_amt = 0
        for s in cart_items['table']:
            total_qty += s['quantity']
            total_amt += s['total_price']

        delivery_amt = 0
        session = request.session
        if "purchase" in request.session:
            id=session["purchase"]["delivery_id"]
            delivery_type = DeliveryOptions.objects.get(id=id)
            delivery_amt = delivery_type.delivery_price
        response = JsonResponse(
            {'cart_items':cart_items['table'], 'total_qty':total_qty, 'total_amt':total_amt, 'delivery_amt':delivery_amt, 'final_total':cart.get_total_cost()})
        return response

@login_required
def cart_detail2(request):
    cart = Cart(request)
    if request.POST.get('action') == 'add':
        productID = request.POST.get('productID')
        productQTY = 1
        product = get_object_or_404(Product, id=productID)
        product_exist = cart.add(product_id=productID, product=product, quantity=productQTY, update_quantity=False)
        response = JsonResponse(
            {'cart_length': cart.__len__()})
        return response
    return None


@login_required
def delivery_and_address(request):
    session = request.session
    mydeliveryopt = {}
    mydeliveryadd = {}
    if "purchase" in request.session:
        delivery_id = session["purchase"]['delivery_id']
        mydeliveryopt = DeliveryOptions.objects.filter(id=delivery_id)
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True).exclude(id=delivery_id)
    else:
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    if "address" in request.session:
        address_id = session["address"]['address_id']
        mydeliveryadd = Address.objects.filter(id=address_id)
        deliveryaddressess = Address.objects.filter(customer=request.user).exclude(id=address_id)
    else:
        deliveryaddressess = Address.objects.filter(customer=request.user)

    serialized_mydeliveryopt = serializers.serialize('python', mydeliveryopt)
    serialized_deliveryoptions = serializers.serialize('python', deliveryoptions)
    serialized_mydeliveryadd = serializers.serialize('python', mydeliveryadd)
    serialized_deliveryaddressess = serializers.serialize('python', deliveryaddressess)


    mydeliveryopt = {}
    deliveryoptions = {}
    mydeliveryadd = {}
    deliveryaddressess = {}
    mydeliveryopt['data_table'] = serialized_mydeliveryopt
    deliveryoptions['data_table'] = serialized_deliveryoptions
    mydeliveryadd['data_table'] = serialized_mydeliveryadd
    deliveryaddressess['data_table'] = serialized_deliveryaddressess

    response = JsonResponse(
        {'deliveryoptions':deliveryoptions, 'deliveryaddressess':deliveryaddressess,
        'mydeliveryopt':mydeliveryopt, 'mydeliveryadd':mydeliveryadd})
    return response


@login_required
def cart_update_address(request):
    session = request.session
    if request.POST.get("action") == "post":
        address_id = str(request.POST.get("address_id"))
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)
        address_type = Address.objects.get(id=address_id)
        if "address" not in session:
            session["address"] = {"address_id": address_id}
        else:
            session["address"]["address_id"] = address_id
            session.modified = True

    if request.POST.get("action") == "delete_address":
        address_id = str(request.POST.get("address_id"))
        Address.objects.filter(customer=request.user, id=address_id).delete()
        if "address" in session:
            if address_id == str(session["address"]["address_id"]):
                del session["address"]
                response = JsonResponse({'address_in_session':'true'})
                return response
    response = JsonResponse({'address_in_session': 'false'})
    return response





