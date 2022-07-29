from django import forms
from django.contrib.auth.models import User
from .models import AccountManager

class UserForm(forms.ModelForm):
    password = forms.CharField(label='Konfirmo Fjalëkalimin', widget=forms.PasswordInput(
        attrs={
        'class': 'form-group',
        'style': 'padding-top: 6px',
        'placeholder': 'konfirmoni fjalëkalimin',
        'type': 'password',
        'name': 'confirmation_password',
        }))
    
    class Meta:
        model = User
        fields = ['password']


class AccountManagerForm(forms.ModelForm):
    
    class Meta:
        model = AccountManager
        fields=[]
