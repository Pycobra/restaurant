from django import forms
from .models import Product,Category

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()

class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(label='Title', min_length=3, max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title', 'id': 'category-title'}))
    parent = forms.CharField(label='Parent', min_length=4, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Parent', 'id': 'category-slug'}))

    class Meta:
        model= Category
        fields=('name', 'parent')

    def clean_title(self):
        title = self.cleaned_data['name'].lower()
        exists= Category.objects.filter(title=title)
        if exists.count():
            raise forms.ValidationError("This title already taken")
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['parent'].required = False


COLOR_CHOICES = (
    ('', 'Select a color'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('White', 'White'),
    ('Black', 'Black'),
    ('Brown', 'Brown'),
    ('Green', 'Green'),
    ('Yellow', 'Yellow'),
    ('Purple', 'Purple'),
    ('Orange', 'Orange'),
    ('Cream', 'Cream'),
    ('Lemon', 'Lemon')
)
class ColorSearchForm(forms.Form):
    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.TextInput(attrs={'class': 'form-control', 'border-radius':'20px',
                                                                          'placeholder': '  choose color1', 'id': 'color-input'}))
class ProductForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=100)
    in_stock = forms.BooleanField(label='In stock:')

    class Meta:
        model = Product
        fields = ['product_type', 'category', 'title', 'description', 'price', 'discount_price', 'in_stock',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Product Type'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Category'})
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Description', 'id':'textarea'})
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Price'})
        self.fields['discount_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Discount Price'})
        self.fields['in_stock'].widget.attrs.update({'id':'checkbox'})
