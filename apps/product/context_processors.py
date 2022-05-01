from .models import Category



def menu_categories(request):
    categories = Category.objects.filter(level=0)
    return {'categories':categories}

    """return {'categories':categories, 'menu_vendor_list':vendor,
            'product_spec_form':ProductSpecForm, 'product_img_form':ProductImageForm}"""


