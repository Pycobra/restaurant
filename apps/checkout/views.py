from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.order.models import OrderReciept, OrderedItemDetail, Address, Checkout
from apps.cart.cart import Cart

from .models import DeliveryOptions, PaymentSelections


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {"delivery_id": delivery_type.id}
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
        response = JsonResponse({"delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if addresses:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].pk)}
        else:
            session["address"]["address_id"] = str(addresses[0].pk)
            session.modified = True
        return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    # print(request.COOKIES)
    session = request.session
    if "address" not in session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        id = session["address"]['address_id']
        address = Address.objects.get(id=id)

    return render(request, "checkout/payment_selection.html", {'address': address})


@login_required
def complete_payment(request):
    # def complete_payment(request: HttpRequest, response: str) -> HttpResponse:
    cart = Cart(request)
    session = request.session
    if request.POST.get('action') == 'post':
        ref = request.POST.get('ref')
        amount = request.POST.get('amount')
        address_id = session["address"]["address_id"]
        delivery_id = session["purchase"]["delivery_id"]
        address = request.user.user_address.get(id=address_id)
        payment_selection = PaymentSelections.objects.get(name='Paystack')
        delivery_instructions = DeliveryOptions.objects.get(id=delivery_id)
        order = OrderReciept.objects.create(
            user_id=request.user.id, delivery_address=address, delivery_instructions=delivery_instructions,
            total_paid=amount, payment_option=payment_selection
        )
        for item in cart:
            OrderedItemDetail.objects.create(order=order, product=item['product'],
                                             amount=item['total_price'], quantity=item['quantity'])
        verified = order.verify_payment(amount, ref)
        print('verified')
        print(verified)
        print('verified')
        if verified:
            order.verified = True
            order.save()
            Checkout.objects.create(order=order, ref=ref)

            messages.success(request, "Payment verification was sucessfull")
        else:
            messages.success(request, "Your payment verification failed")
        return redirect('.')