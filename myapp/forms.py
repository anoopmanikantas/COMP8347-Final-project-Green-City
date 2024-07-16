# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AdminUser, BuildingPermit, CustomUser


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


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required')


class BuildingPermitForm(forms.ModelForm):
    class Meta:
        model = BuildingPermit
        fields = ['name', 'contact_number', 'mail_id', 'city', 'province', 'area', 'floors', 'government_id_proof',
                  'land_purchase_record']

        widgets = {
            'area': forms.Select(choices=BuildingPermit.AREA_CHOICES),
            'floors': forms.Select(choices=BuildingPermit.FLOORS_CHOICES),
        }
