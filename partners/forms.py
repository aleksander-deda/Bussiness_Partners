from django import forms
from .models import Partner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from betterforms.multiform import MultiModelForm


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password"]



class PartnerForm(forms.ModelForm):
    
    class Meta:
        model = Partner
        fields = ['nr_tel']


class UserPartnerMultiForm(forms.ModelForm):
    class Meta:
        fields=["username", "email", "password1", "nr_tel"]
        form_classes = {
            'user': UserForm,
            'partner': PartnerForm,
    }