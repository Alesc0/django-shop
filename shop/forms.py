from django import forms

class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

class comercialUserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    widget=forms.Select(choices=((1,'Comercial 1'),(2,'Comercial 2')))
    type = forms.IntegerField(widget=widget)
    company = forms.CharField()

class addProductForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    stock = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    image = forms.ImageField()
    
class checkoutBillingForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    zip = forms.CharField()
    country = forms.CharField()
    phone = forms.CharField()
    same_as_billing = forms.BooleanField(required=False)

class checkoutShippingForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    zip = forms.CharField()
    country = forms.CharField()
    phone = forms.CharField()