# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AdminUser

class AdminSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = AdminUser
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'username', 'password1', 'password2')

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)
