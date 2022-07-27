from django import forms
from .models import Partner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from backoffice.models import Member


class PartnerForm(forms.ModelForm):
    
    class Meta:
        model = Partner
        fields=[ 'nr_tel']

