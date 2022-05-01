from decimal  import Decimal

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core import serializers


from .models import Category, Product, ProductType
from .forms import AddToCartForm, AddCategoryForm, ColorSearchForm, ProductForm

from apps.cart.cart import Cart


def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)
    instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    product = Product.objects.filter(
        category__in=Category.objects.filter(name=instance.name).get_descendants(include_self=True))
    brands = ProductType.objects.all()
    return render(request, 'product/search.html', {'product_search': product, 'product_search_query': instance
                                                   , 'brands':brands})


def all_product(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        product = Product.objects.filter(category__id=id)

        serialized_queryset = serializers.serialize('python', product)
        place = {}
        place['table'] = serialized_queryset

        response = JsonResponse({'place': place})
        return response

def single_product(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        product = Product.objects.filter(id=id)

        serialized_queryset = serializers.serialize('python', product)
        place = {}
        place['table'] = serialized_queryset
        response = JsonResponse({'place': place})
        return response


def product_detail(request, category_slugz, product_slugz):
    cart = Cart(request)
    products = get_object_or_404(Product, category__slug=category_slugz, slug=product_slugz, is_active=True)

    wishlist = products.users_wishlist.all().count()
    likes = products.likes.all().count()
    product_id = str(products.id)
    wishlist_boolean = False
    like_boolean = False

    if products.users_wishlist.filter(id=request.user.id).exists():
        wishlist_boolean=True
    if products.likes.filter(id=request.user.id).exists():
        like_boolean=True

    #-------------------------------------------------
    breadcrumbs_link = products.get_cat_list()
    category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
    breadcrumbs = zip(breadcrumbs_link, category_name)
    return render(request, 'product/product.html', {'product': products, 'product_id': product_id, 'wishlist': str(wishlist),
                                                    'wishlist_boolean':wishlist_boolean, 'likes': str(likes), 'like_boolean':like_boolean,
                                                    'breadcrumbs': breadcrumbs})


def product_detail2(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        qtyAction = request.POST.get('qtyAction')
        productID = int(request.POST.get('productID'))
        productQTY = int(request.POST.get('productQTY'))
        if qtyAction == 'include_item':
            product = get_object_or_404(Product, id=productID)
            cart.add(product_id=productID, product=product, quantity=productQTY, update_quantity=False)
            messages.success(request, 'The account was successfully added to the account')
            response = JsonResponse(
                {'cart_length': cart.__len__()})
            return response

@login_required
def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                vendor = form.save(commit=False)
                title = form.cleaned_data['title']
                slug = form.cleaned_data['slug']
                Category.objects.create(title=title, slug=slug, ordering='1')
        else:
            form=AddCategoryForm()
        return render(request,'product/add_category.html', {'form':form})
    else:
        return redirect('core_:frontpage')

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'product/category.html', {'category_in_product_view': category})


@login_required
def likes_add_and_remove(request, id):
    if request.GET.get('action') == 'get':
        product = get_object_or_404(Product, id=id)
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            product_exist = True
            action_text='<i class="fa fa-heart-o" id="icon2" style="color:var(--lightblue);"> like</i>'
        else:
            product.likes.add(request.user)
            product_exist = False
            action_text='<i class="fa fa-heart-o" id="icon2" style="color:var(--lightblue);"> unlike</i>'
        likes = product.likes.all().count()
        print('likes')
        print(likes)
        print('likes')
        response = JsonResponse({'likes_no': str(likes), 'action_text':action_text, 'product_exist':product_exist})
        return response

@login_required
def remove_from_likes(request):
    if request.GET.get('action') == 'get':
        id = request.GET.get('productID')
        product = get_object_or_404(Product, id=id)
        product_count=product.likes.add(request.user).count()
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            messages.success(request, "you have unliked " + product.title)
    response = JsonResponse({'product_count':product_count})
    return response

@login_required
def add_product(request):
    vendor = request.user.which_vendor
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            product.vendor = vendor
            product.title = product.title
            product.category = product.category
            product.slug = slugify(product.title)
            product.description = product.description
            product.price = Decimal(product.price)
            product.in_stock = True
            product.is_active = True
            product.save()
            return redirect('vendor_:vendor_admin_')
    else:
        form=ProductForm()
    return render(request,'vendor/add_product.html', {'form':form})

@login_required
def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                vendor = form.save(commit=False)
                title = vendor.cleaned_data['title']
                slug = vendor.cleaned_data['slug']
                Category.objects.create(title=title, slug=slug, ordering='1')
        else:
            form=AddCategoryForm()
        return render(request,'product/add_category.html', {'form':form})
    else:
        return redirect('core_:frontpage')
