from django.db import models
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from apps.account.models import UserBase



class DeliveryOptions(models.Model):
    """
    The Delivery methods table contining all delivery
    """

    DELIVERY_METHODS = [
        ("In Store", "In Store"),
        ("Home Delivery", "Home Delivery"),
    ]
    DELIVERY_NAMES = [
        ("NONE", ""),
        ("Standard Delivery", "Standard Delivery"),
        ("Next Day Delivery", "Next Day Delivery"),
        ("Week Delivery", "Week Delivery"),
    ]
    PRICE_CHOICES = [
        ("Island", 150),
        ("Mainland", 200),
        ("Outliers", 250),
        ("NW", 1500),
        ("NE", 1500),
        ("NC", 1500),
        ("SW", 1000),
        ("SE", 1000),
        ("SS", 1000),
        """("NONE", Decimal(0)),
        ("IS", Decimal(15.00)),
        ("ML", Decimal(20.00)),
        ("OL", Decimal(25.00)),
        ("NW", Decimal(150.00)),
        ("NE", Decimal(150.00)),
        ("NC", Decimal(150.00)),
        ("SW", Decimal(100.00)),
        ("SE", Decimal(100.00)),
        ("SS", Decimal(100.00)),"""
    ]
    TIME_FRAME_CHOICES = [
        ("24hours", "24hours"),
        ("48hours", "48hours"),
        ("72hours", "72hours"),
    ]
    REGION_CHOICES = [
        ("None", ""),
        ("Island", "Island"),
        ("Mainland", "Mainland"),
        ("Outliers", "Outliers"),
        ("NW", "North West"),
        ("NE", "North East"),
        ("NC", "North Central"),
        ("SW", "South West"),
        ("SE", "South East"),
        ("SS", "South South"),
    ]
    WINDOW_CHOICES = [
        ("None", ""),
        ("5.00am", "5.00am to 10.00pm"),
        ("10.00am", "10.00am to 3.00pm"),
        ("3.00pm", "3.00pm to 7.00pm"),
        ("7.00pm", "7.00pm to 12.00pm"),
    ]
    delivery_name = models.CharField(choices=DELIVERY_NAMES,verbose_name=_("delivery_name"),help_text=_("Required"),max_length=255,)
    delivery_region = models.CharField(choices=REGION_CHOICES, null=True,verbose_name=_("delivery_location"),help_text=_("Required"),max_length=255,)
    delivery_price = models.IntegerField(verbose_name=_("delivery price"))
    #delivery_price = models.DecimalField(verbose_name=_("delivery price"),help_text=_("Maximum 999.99"),
    #    error_messages={
    #        "name": {"max_length": _("The price must be between 0 and 999.99."),},
    #    },
    #    max_digits=5,
    #    decimal_places=2,
    #)"""
    delivery_method = models.CharField(choices=DELIVERY_METHODS,verbose_name=_("delivery_method"),help_text=_("Required"),max_length=255,)
    delivery_timeframe = models.CharField(choices=TIME_FRAME_CHOICES,verbose_name=_("delivery timeframe"),help_text=_("Required"),max_length=255,)
    delivery_window = models.CharField(choices=WINDOW_CHOICES,verbose_name=_("delivery window"),help_text=_("Required"),max_length=255,)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    PAYMENT_SELECTIONS = [
        ("Paystack", "Paystack"),
        ("Paypal", "Paypal"),
        ("Stripe", "Stripe"),
    ]
    name = models.CharField(choices=PAYMENT_SELECTIONS, verbose_name=_("name"), help_text=_("Required"), max_length=255,)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name
