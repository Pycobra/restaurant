from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import login, logout

from apps.product.models import Product, Category
from apps.account.forms import UserLoginForm, RegistrationForm

from apps.checkout.models import DeliveryOptions
from apps.order.models import Address


def frontpage(request):
    """if request.method == "POST":
        userLoginForm = UserLoginForm(request.POST)
        print(userLoginForm)
        if userLoginForm.is_valid():
            print('AAAAAAAAAAAAAa')
            user=userLoginForm.save(commit=False)
            login(request, user)"""

    session = request.session
    mydeliveryopt = {}
    mydeliveryadd = {}
    if "purchase" in request.session:
        delivery_id = session["purchase"]['delivery_id']
        mydeliveryopt = DeliveryOptions.objects.get(id=delivery_id)
    if "address" in request.session:
        address_id = session["address"]['address_id']
        mydeliveryadd = Address.objects.get(id=address_id)

    #all_products = Product.objects.prefetch_related("product_images").filter(is_active=True, in_stock=True).order_by('-created_at')
    all_products = Product.objects.filter(is_active=True, in_stock=True).order_by('-created_at')
    categories = Category.objects.filter(level=0)
    return render(request, 'core/frontpage.html', {'all_products': all_products, 'categories':categories, 'form':UserLoginForm, 'registerform':RegistrationForm,
                                                   'mydeliveryopt':mydeliveryopt, 'mydeliveryadd':mydeliveryadd})

