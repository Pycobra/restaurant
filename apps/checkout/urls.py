from django.urls import include, path
from django.conf.urls import url

from . import views

app_name = "checkout_"

urlpatterns = [
    path("delivery-choices", views.deliverychoices, name="delivery_choice"),
    path("cart_update_delivery/", views.cart_update_delivery, name="cart_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("all", views.complete_payment, name="complete_payment2"),
]
