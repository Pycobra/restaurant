#from django.contrib.auth.models import User
import secrets

from django.conf import settings
from django.db import models
#django_countries.fields import CountryField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.mail import send_mail


#from apps.vendor.models import Vendor

#from .paystack import Paystack


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('email address'),max_length=150, unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    unique_id=  models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=150, null=True)
    surname = models.CharField(max_length=50, null=True)
    user_image= models.ImageField(verbose_name=_("profile image"),
                               help_text=_("Upload a your image"),
                               upload_to="images/uploads/profile/", default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    mobile = models.CharField(max_length=20, blank=True)
    #following= models.ManyToManyField("Vendor", related_name="following", blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering=['user_name']

    def save(self, *args, **kwargs) -> None:
        while not self.unique_id:
            unique_id = secrets.token_urlsafe(33)
            object_with_similar_order_key = UserBase.objects.filter(unique_id=unique_id).exists()
            if not object_with_similar_order_key:
                self.unique_id = unique_id
        super().save(*args, **kwargs)


    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            '1@1.com',
            [self.email],
            fail_silently=False,
        )
    #dunder
    #to make this the models name at admin area || and how to reference this model
    def __str__(self):
        return self.user_name




