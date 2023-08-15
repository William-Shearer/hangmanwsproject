from django import forms
from django.forms import ModelForm
from .models import *

"""
Here is the best way yet to do quick and dirty forms for models.
There is a specific one for login, but for this example, the technique holds good.
"""
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {"password": forms.PasswordInput()}

"""
Here is a standard one, to not forget.
"""
class RegisterForm(forms.Form):
    username = forms.CharField(label = "User Name * ", max_length = 50, required = True, widget = forms.TextInput(attrs = {"autofocus": True}))
    first_name = forms.CharField(label = "First Name ", max_length = 50, required = False, widget = forms.TextInput())
    last_name = forms.CharField(label = "Last Name ", max_length = 50, required = False, widget = forms.TextInput())
    email = forms.EmailField(label = "e-mail * ", required = True, widget = forms.EmailInput())
    password = forms.CharField(label = "Password * ", max_length = 50, required = True, widget = forms.PasswordInput())
    confirmation = forms.CharField(label = "Confirm Password * ", max_length = 50, required = True, widget = forms.PasswordInput())

