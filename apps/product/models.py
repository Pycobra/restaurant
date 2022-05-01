from django.urls import reverse
from django.template.context_processors import request
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify


from apps.account.models import UserBase






class Category(MPTTModel):
    """
    Category Table implementated with MPTT
    """
    name = models.CharField( verbose_name=_("Category Name"), help_text=_("Required and unique"), max_length=255)
    slug = models.SlugField(verbose_name=_("Category safe url"), max_length=255)
    parent = TreeForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]
    class Meta:
        """enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent',)"""
        verbose_name =_("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs


    def get_absolute_url(self):
        return reverse('product_:category_list', args=[self.slug])

class ProductType(models.Model):
    """
    ProductType Table ll provide a list of the different types
    of products that are for sale.
    """
    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name =_("Product Type")
        verbose_name_plural = _("Product Types")
    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, related_name='vendors_product_type', on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    slug = models.SlugField(max_length=255)
    images = models.ImageField(verbose_name=_("image"), help_text=_("Upload a product image"),
                               upload_to="images/uploads/", default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    ingredient = models.TextField(verbose_name=_("ingredient"), help_text=_("Not Required"), blank=True)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    price = models.IntegerField(verbose_name=_("Regular price"), help_text=_("Maximum 999.99"),
                                error_messages={
                                    "name": {"max_length": _("The price must be between 0 and 999.99.")},
                                })
    discount_price = models.IntegerField(verbose_name=_("Discount price"), help_text=_("Maximum 999.99"),
                                error_messages={
                                    "name": {"max_length": _("The price must be between 0 and 999.99.")},
                                })
    discount_percent = models.IntegerField(verbose_name=_("Discount percent"), null=True)
    price_difference = models.IntegerField(verbose_name=_("Price difference"), null=True)
    in_stock = models.BooleanField(verbose_name=_("Product availability"), help_text=_("Change product availability"), default=True)
    is_active = models.BooleanField(verbose_name=_("Product visibility"), help_text=_("Change product visibility"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(UserBase, related_name="user_wishlist", blank=True)
    likes = models.ManyToManyField(UserBase, related_name="likes", blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name =_("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def get_absolute_url(self):
        return reverse('product_:product_detail_', args=[self.category, self.slug])


def presaver(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
    if instance.discount_price:
        new = ((int(instance.discount_price) / int(instance.price)) * 100)
        discount_percent = (100 - new)
        price_difference = (int(instance.price) - int(instance.discount_price))
        instance.discount_percent = discount_percent
        instance.price_difference = price_difference

pre_save.connect(presaver, sender=Product)

"""
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField(verbose_name=_("image"), help_text=_("Upload a product image"),
                               upload_to="images/uploads/", default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name =_("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.product.title
"""
