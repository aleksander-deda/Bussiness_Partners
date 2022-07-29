from django import forms
from .models import Partner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from backoffice.models import Member

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

class PartnerForm(forms.ModelForm):
    
    class Meta:
        model = Partner
        fields=['nr_tel']

