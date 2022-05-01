from django.urls import path
from . import views
from django.conf.urls import url
from .templatetags import searching


app_name="product_"
urlpatterns = [
    path('all-product/', views.all_product, name="all_product"),
    path('single-product/', views.single_product, name="single_product"),
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    path('<slug:category_slugz>/<slug:product_slugz>/', views.product_detail, name="product_detail_"),
    path('', views.product_detail2, name="product_detail2_"),
    path('<slug:category_slug>/', views.category_list, name="category_list_"),
    path('add-product/', views.add_product, name="add_product_"),
    path('add-category/', views.add_category, name="add_category_"),
    path('likes_add_and_remove/<int:id>', views.likes_add_and_remove, name="likes_add_and_remove"),
    path("likes/remove_from_likes/", views.remove_from_likes, name="remove_from_likes"),
]
