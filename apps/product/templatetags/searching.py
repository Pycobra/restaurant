from django import template
register = template.Library()


from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from ..models import Product

@register.filter(needs_autoescape=True)
def search_for(request):
    if request.GET.get('action') == 'post':
        query = request.GET.get('productID')
        print(query)
        print("BAD THUGZ LIVETHo")
        product_search = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        """|
                                     Q(category__icontains=query) | Q(price__icontains=query) |
                                     Q(product_type__icontains=query))"""

        product = f"""
                <div class="box-body">
                    {{% for i in product_search %}}
                    <a href="{{% url 'product_:product_detail_' i.category.slug i.slug %}}"class="">
                        <div class="card">
                            {{% for image in i.product_images.all %}}
                            {{% if image.is_main %}}
                            <div class="card-img">
                                <span>10%</span>
                                <img src="{{ image.images.url }}" alt="{{ image.images.alt_text }}"
                            </div>
                            <div class="card-text">
                                <h2 class="subtitle"> {{i.description}} </h2>
                                <span> NGstoreboy Price Now</span>
                                <h3 class="price is-size-6 mb-5"> {{i.price}} </h3>
                                <h3 class="price is-size-6 mb-5"> {{i.discount_price}} </h3>
                                <button class="is-uppercase">ADD TO CART</button>
                            </div>
                            {{% endif %}}
                            {{% endfor %}}
                        </div>
                    </a>
                    {{% endfor %}}
                </div>"""
        response = JsonResponse({'product_search': product})
        return response
