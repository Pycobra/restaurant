import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core import serializers

from apps.order.models import Address
from .forms import RegistrationForm, ProfileEditForm, UserLoginForm, ImageEditForm
from .models import UserBase
from .token import account_activation_token

from apps.product.models import Product, Category
from apps.order.models import OrderReciept, Address


import re
def registration_check2(request):
    content = request.GET.get('content')
    if request.GET.get('action') == 'check_username':
        it_exists = UserBase.objects.filter(user_name__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
    if request.GET.get('action') == 'check_email':
        it_exists = UserBase.objects.filter(email__exact=content).exists()
        ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', content)
        print(f'correctly ends_with ({ends_with})')
        if ends_with != None:
            result2 = content.split('@')
            stri1 = ''
            stri2 = ''
            for i in result2:
                stri1 += i
            stri1 = stri1.split('.')
            for i in stri1:
                stri2 += i
            print(f'stripped result ({stri2})')
            contains_non_alpha_num = re.search(r"\W[-_/]", stri2)
            print('===============alpha & number container----------------------------')
            print(contains_non_alpha_num)
            if contains_non_alpha_num != None:
                print('===============yes contains non alpha & digit---------------------')

                unwanted_characterz = ['~', '@', '#', '$', '%', '^', '&', '*', '(', ')', \
                                       '_', '-', '+', '=', '[', ']', '{', '}', '|', '', ":", \
                                       ";", '"', "'", '<', ",", '>', ".", "/", "?"]
                contain_unwanted_characterz = False

                contains_the_required_chars = re.search(r"[-_/]", stri2)
                print(f'chars_container is ({contains_the_required_chars})')
                for i in stri2:
                    if i in unwanted_characterz:
                        print('===============it contains the required char---------------------')
                        contain_unwanted_characterz = True
                        return JsonResponse({'exists': it_exists})
                    break
                if contains_the_required_chars != None and not contain_unwanted_characterz:
                    print('===============it contains the required char---------------------')
                    return JsonResponse({'exists': it_exists})
        else:
            return JsonResponse({'exists': it_exists})
        # re.search(r"content{1}", "geeks")
        # {p} Matches the expression to its left p times, and not less.
        # \w Matches alphanumeric characters, that is a - z, A - Z, 0 - 9, and underscore(_)
        # \W Matches non - alphanumeric characters, that is except a - z, A - Z, 0 - 9 and _
        # \d Matches digits, from 0-9.
        # \D Matches any non-digits.
        # \s Matches whitespace characters, which also include the \t, \n, \r, and space characters.
        # \S Matches non-whitespace characters.
        # [a-z0-9]Matches characters from a to z or from 0 to 9.
        # [(+*)]Special characters become literal inside a set, so this matches (, +, *, or )
    if request.GET.get('action') == 'check_password':
        it_exists = UserBase.objects.filter(password__exact=content).exists()
        if ends_with != None:
            result2 = content.split('@')
            stri1 = ''
            stri2 = ''
            for i in result2:
                stri1 += i
            stri1 = stri1.split('.')
            for i in stri1:
                stri2 += i
            print(f'stripped result ({stri2})')
            contains_non_alpha_num = re.search(r"\W[-_/]", stri2)
            print('===============alpha & number container----------------------------')
            print(contains_non_alpha_num)
            if contains_non_alpha_num != None:
                print('===============yes contains non alpha & digit---------------------')

                unwanted_characterz = ['~', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                                       '_', '-', '+', '=', '[', ']', '{', '}', '|', '', ":",
                                       ";", '"', "'", '<', ",", '>', ".", "/", "?"]
                contain_unwanted_characterz = False

                contains_the_required_chars = re.search(r"[-_/]", stri2)
                print(f'chars_container is ({contains_the_required_chars})')
                for i in stri2:
                    if i in unwanted_characterz:
                        print('===============it contains the required char---------------------')
                        contain_unwanted_characterz = True
                        return JsonResponse({'exists': it_exists})
                    break
                if contains_the_required_chars != None and not contain_unwanted_characterz:
                    print('===============it contains the required char---------------------')
                    return JsonResponse({'exists': it_exists})
        else:
            return JsonResponse({'exists': it_exists})

        response = JsonResponse({'exists': it_exists})
    if request.GET.get('action') == 'check_password2':
        it_exists = UserBase.objects.filter(password2__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
        char = ["/", '.', '-', '_']
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    return response

def registration_check(request):
    content = request.GET.get('content')
    if request.GET.get('action') == 'check_username':
        it_exists = UserBase.objects.filter(user_name__exact=content).exists()
        contains_characters = re.search(r"\W", content)
        if not it_exists:
            if len(content) >= 4:
                if contains_characters != None:
                    return JsonResponse({'msg_type':False, 'msg': 'Username must not include characters'})
                else:
                    return JsonResponse({'msg_type': True, 'msg': ''})
            else:
                return JsonResponse({'msg_type': False, 'msg': 'Username must be 4 or more characters'})
        else:
            return JsonResponse({'msg_type':False, 'msg': 'Username is already in use'})


    contain_unwanted_characterz = False
    if request.GET.get('action') == 'check_email':
        it_exists = UserBase.objects.filter(email__exact=content).exists()
        if not it_exists:
            contain_unwanted_characterz =False
            #checks & executes if it contains characters
            contains_non_characters = re.search(r"\W", content)
            if contains_non_characters != None:
                unwanted_characterz = ['~', '!', '#', '$', '%', '^', '&', '*', '(', ')', \
                             '+', '=', '[', ']', '{', '}', '|', '', ":", ";", '"', "'", \
                               '<', ",", '>', "?"]

                for i in content:
                    if i in unwanted_characterz:
                        contain_unwanted_characterz =True
                        break
            if contain_unwanted_characterz == True:
                return JsonResponse({'msg_type':False, 'msg': 'Email contain unwanted character'})

            # checks & executes if it doesnt contains characters at all / bad character
            elif contain_unwanted_characterz == False:
                ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', content)
                if ends_with != None:
                    return JsonResponse({'msg_type':True, 'msg': ''})
                else:
                    return JsonResponse({'msg_type':False, 'msg': "Email end contains wrong pattern, use ('gmail.com' etc)"})

        else:
            return JsonResponse({'msg_type':False, 'msg': 'Email is already in use'})


    if request.GET.get('action') == 'check_password':
        it_exists = UserBase.objects.filter(password__exact=content).exists()
        contains_characters = re.search(r"\W", content)
        contains_digit = re.search(r"\d", content)
        contains_white_space = re.search(r"\s", content)
        if len(content) >= 8:
            if contains_characters == None:
                return JsonResponse({'msg_type':False, 'msg': 'Password must include characters'})
            if contains_digit != None:
                print('cyyyyyyyyyyyyyyyyyyyyyyy')
            if contains_digit == None:
                return JsonResponse({'msg_type':False, 'msg': 'Password must include digits'})
            if contains_white_space != None:
                return JsonResponse({'msg_type':False, 'msg': 'Password allows no white space'})
            else:
                return JsonResponse({'msg_type':True, 'msg': ''})
        else:
            return JsonResponse({'msg_type':False,'msg': 'password must be longer than 8 characters'})
    if request.GET.get('action') == 'check_password2':
        it_exists = UserBase.objects.filter(password2__exact=content).exists()
        response = JsonResponse({'exists': it_exists})
        char = ["/",'.','-','_']
        num = [1,2,3,4,5,6,7,8,9,0]

    return JsonResponse({'exists': it_exists})


def account_registration(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        registrationform = RegistrationForm(request.POST)
        if registrationform.is_valid():
            user=registrationform.save(commit=False)
            user.email=registrationform.cleaned_data['email']
            user.set_password(registrationform.cleaned_data['password'])
            user.is_active=False
            user.save()

            current_site=get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/registration/account_activation_email.html', {
                      'user':user,
                      'domain': current_site.domain,
                      'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                      'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('core_:frontpage')
    else:
        registrationform=RegistrationForm()
    return render(request, 'account/registration/register.html', {'form':registrationform})

def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user=UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return render(request, 'account/registration/account_activation_invalid.html')



@login_required
def add_address(request):
    session = request.session
    if request.POST.get('action') == 'post':
        full_name = request.POST.get('full_name')
        city = request.POST.get('city')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        postal_code = request.POST.get('postal_code')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        if (len(full_name) != 0 and len(city) != 0 and len(email) != 0 and len(phone) != 0 and len(
            postal_code) != 0 and len(address_line1) != 0 and len(address_line2) != 0):
            my_add = Address.objects.create(customer=request.user, full_name=full_name, city=city, email=email,
                               phone=phone, postal_code=postal_code, address_line1=address_line1, address_line2=address_line2)
            response = JsonResponse(
                {'null': False, 'full_name': my_add.full_name, 'city': my_add.city, 'email': my_add.email,
                 'phone': my_add.phone,
                 'postal_code': my_add.postal_code, 'address_line1': my_add.address_line1,
                 'address_line2': my_add.address_line2})
            return response
        elif (len(full_name) != 0 and len(city) != 0 and len(email) != 0 and len(phone) != 0 and len(
                postal_code) != 0 and len(address_line1) != 0):
            my_add = Address.objects.create( customer=request.user, full_name=full_name, city=city, email=email,
                                   phone=phone, postal_code=postal_code, address_line1=address_line1)
            response = JsonResponse({'null': False, 'full_name':my_add.full_name, 'city':my_add.city, 'email':my_add.email, 'phone':my_add.phone,
                                     'postal_code':my_add.postal_code, 'address_line1':my_add.address_line1})
            return response
    response = JsonResponse({'null': True})
    return response

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("cart_:cart_details"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserEditAddressForm(instance=address)
    return render(request, "account/user/edit_address.html", {"form": address_form})


@login_required
def set_default(request):
    if request.POST.get('action') == 'post':
        address_id = request.POST.get('address_id')
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)

    response = JsonResponse({'address_id':address_id})
    return response

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = OrderReciept.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

