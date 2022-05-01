from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.template.context_processors import request

import re
import timeit

from apps.order.models import Address
from .models import UserBase



class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Username', min_length=4,  max_length=50, help_text='Required')
    email = forms.EmailField(label='Email', max_length=100, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model= UserBase
        fields=('user_name', 'email', 'password', 'password2')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        exists= UserBase.objects.filter(user_name=user_name)
        if exists.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    def clean_password2(self):
        passwords = self.cleaned_data
        if passwords['password'] != passwords['password2']:
            raise forms.ValidationError("Both passwords do not match")
        return passwords['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken, please use another Email0")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Username', 'id': 'signup-username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Email', 'name': 'email', 'id': 'signup-email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'password', 'id': 'signup-pwd'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Repeat Password', 'id': 'signup-pwd2'})


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'placeholder': 'Password', 'id': 'login-pwd'}))

    class Meta:
        model= UserBase
        fields=('username', 'password')

    """def clean_password(self):
        passwords = self.cleaned_data
        if UserBase.objects.filter(user=request.user).exists():
        if passwords['password'] != passwords['password2']:
            raise forms.ValidationError("Both passwords do not match")
        return passwords['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken, please use another Email0")
        return email"""

class ImageEditForm(forms.ModelForm):
    class Meta:
        model= UserBase
        fields=('user_image',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_image'].widget.attrs.update(
            {'class':'none', 'id':'none', 'help-text': ''})


class ProfileEditForm(forms.ModelForm):
    firstname = forms.CharField(label='Firstname:', min_length=4, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'firstname', 'id': 'login'
                                                                              'edit-username'}))
    surname = forms.CharField(label='Surname:', min_length=4, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'surname', 'id': 'login'
                                                                              'edit-username'}))
    """user_name = forms.CharField(label='Username*', min_length=4, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'login'
                                                                              'edit-username'}))"""
    mobile = forms.CharField(label='Phone no:', min_length=7, max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone no', 'id': 'login'
                                                                          'edit-phone'}))

    class Meta:
        model= UserBase
        fields=('firstname', 'surname', 'mobile',)

    def clean_firstname(self):
        """

        #[x for x in mylist if not any(c.isdigit() for c in x)]
        mylist=['hello', 'we12', 'reset', '909', 'q00q']
        def isalpha(mylist):
            return [s for s in mylist if not s.isalpha()]
        def fisalpha(mylist):
            return filter(str.isalpha.mylist)
        def reregex(mylist, myregex = re.compile(r'\d')):
            return [s for s in mylist if not myregex.search(s)]
        def isdigit(mylist, myregex = re.compile(r'\d')):
            return [x for x in mylist if not any(c.isdigit() for c in x)]

        for func in ('isalpha', 'fisalpha', 'reregex', 'isdigit'):
            print func, timeit.timeit(func+'(my_list)', 'from __main__ import my_list,'+func)
        """
        firstname = self.cleaned_data['firstname']
        if not firstname.isalpha():
            raise forms.ValidationError("firstname cannot contain digits or character")
        return firstname
    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if not surname.isalpha():
            raise forms.ValidationError("surname cannot contain digits or character")
        return surname
    """def clean_user_name(self):
        username = self.cleaned_data['user_name'].lower()
        #if UserBase.objects.filter(user_name=request.user.username).exists():
        #    raise forms.ValidationError("you have used this username already, please use another username")
        if UserBase.objects.filter(user_name=username).exists():
            raise forms.ValidationError("username already taken, please use another username")
        return username"""

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit():
            raise forms.ValidationError("phone no cannot contain alphabets or character")
        return mobile

    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True"""


class UserAddressForm(forms.ModelForm):
    full_name = forms.CharField(label='Fullname', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    phone = forms.CharField(label='Phone', min_length=7, max_length=25, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    address_line1 = forms.CharField(label='Address', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    address_line2 = forms.CharField(label='Address2', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    town_city = forms.CharField(label='Town/City', min_length=2, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    post_code = forms.CharField(label='Postcode', min_length=2, max_length=20, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))


    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line1", "address_line2", "town_city", "post_code"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Last Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line1"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["post_code"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )



class UserEditAddressForm(forms.ModelForm):
    full_name = forms.CharField(label='Fullname:', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Fullname'}))
    town_city = forms.CharField(label='Town/City:', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Town/City'}))
    phone = forms.CharField(label='Phone no:', min_length=7, max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone no'}))
    post_code = forms.CharField(label='Postcode:', min_length=2, max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Postcode'}))
    address_line1 = forms.CharField(label='Address line1:', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address1'}))
    address_line2 = forms.CharField(label='Address line2:', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address2'}))

    class Meta:
        model= Address
        fields=('full_name', 'town_city', 'phone', 'post_code', 'address_line1', 'address_line2')

    def clean_address_line1(self):
        address_line1 = self.cleaned_data['address_line1']
        if Address.objects.filter(address_line1=address_line1).exists():
            raise forms.ValidationError("address already in use, please use another address")
        return address_line1

    def clean_address_line2(self):
        address_line2 = self.cleaned_data['address_line2']
        if Address.objects.filter(address_line2=address_line2).exists():
            raise forms.ValidationError("address already in use, please use another address")
        return address_line2

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("phone can contain only digits")
        return phone

    def clean_postcode(self):
        postcode = self.cleaned_data['post_code']
        if not postcode.isdigit():
            raise forms.ValidationError("postcode can contain only digits")
        return postcode





class PassResetForm(PasswordResetForm):
    email = forms.EmailField(label='Account email (can not be changed)', widget=forms.TextInput(
            attrs={'class': 'form-input', 'placeholder': 'Enter your email address', 'id': 'reset-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("unfortunately we cannot find that Email address ")
        return email


class PassResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password', 'id': 'new-pwd1'}))
    new_password2 = forms.CharField(label='Repeat password', widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password', 'id': 'new-pwd2'}))


    class Meta:
        model= UserBase
        fields=('new_password1', 'new_password2')