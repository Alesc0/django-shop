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
    widget=forms.Select(choices=((1,'Comercial 1'),(2,'Comercial 2'),(3,'Partner')))
    type = forms.IntegerField(widget=widget)
    company = forms.CharField(required=False)

class admin_user_form(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    widget=forms.Select(choices=((1,'Comercial 1'),(2,'Comercial 2'),(3,'Partner'),(4,'Admin'),(5,'User')))
    type = forms.IntegerField(widget=widget)
    company = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)

class admin_edit_user_form(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    reset_password = forms.CharField(required=False,widget=forms.PasswordInput)
    widget=forms.Select(choices=((1,'Comercial 1'),(2,'Comercial 2'),(3,'Partner'),(4,'Admin'),(5,'User')))
    type = forms.IntegerField(widget=widget)
    company = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)


class productForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    stock = forms.IntegerField(min_value=0)
    promo = forms.IntegerField(min_value=0,max_value=100)
    price = forms.IntegerField(min_value=0)
    image = forms.ImageField(required=False)

class checkoutBillingForm(forms.Form):
    nif = forms.CharField()
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    same_for_shipping = forms.BooleanField(required=False)
    

class checkoutShippingForm(forms.Form):
    address = forms.CharField()
    city = forms.CharField()
    zip = forms.CharField()
    country = forms.CharField()