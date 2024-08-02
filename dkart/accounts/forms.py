from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    model = Account
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']