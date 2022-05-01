from django import forms

class CheckoutForm(forms.ModelForm):
    first_name = forms.CharField(label='Firstname', min_length=2,  max_length=50, help_text='Required', error_messages={'required':'Sorry, firstname'})
    last_name = forms.CharField(label='Lastname', min_length=2,  max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    email = forms.EmailField(label='Email', max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    address = forms.CharField(label='Address', min_length=4,  max_length=50, error_messages={'required':'Sorry, you will need an email'})
    zipcode = forms.CharField(label='Zipcode', min_length=4,  max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    place = forms.CharField(label='City', min_length=4,  max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    phone = forms.CharField(label='Phone No', min_length=4,  max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    stripe_token = forms.CharField(label='Stripe Token', min_length=4,  max_length=50, help_text='Required')

