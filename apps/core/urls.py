from django.urls import path
from . import views

app_name="core_"
urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    # #path('contact/', views.contact, name="contact"),
    # #path('search/<slug:category>/', views.category_search, name="category_search"),
    # #path("<slug:user_unique_id>/<slug:logged_in_user_unique_id>/error", communication.views.send_message, name="send_msg"),
]
