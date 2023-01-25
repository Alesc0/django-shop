from django import forms

class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

class customUserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    widget=forms.Select(choices=((1, 'User'),(2, 'Admin'),(3,'Comercial 1'),(4,'Comercial 2')))
    type = forms.IntegerField(widget=widget)

class addProductForm(forms.Form):
    name = forms.CharField()
    price = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()