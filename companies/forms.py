# from typing import Any, Mapping
from django import forms
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from .models import Company

class CompanyForm(forms.ModelForm):

   class Meta:
      model = Company
      fields = ['name', 'cuit', 'clanae_code', 'surveyor', 'address_street', 'address_number', 'city', 'zip_code', 'phone', 'email']
      widgets = {
         'name': forms.TextInput(attrs={'class':'form-control'}),
         'cuit': forms.TextInput(attrs={'class':'form-control'}),
         'clanae_code': forms.NumberInput(attrs={'class':'form-control'}),
         'surveyor': forms.Select(attrs={'class':'form-control'}),
         'address_street': forms.TextInput(attrs={'class':'form-control'}),
         'address_number': forms.TextInput(attrs={'class':'form-control'}),
         'city': forms.TextInput(attrs={'class':'form-control'}),
         'zip_code': forms.NumberInput(attrs={'class':'form-control'}),
         'phone': forms.TextInput(attrs={'class':'form-control'}),
         'email': forms.TextInput(attrs={'class':'form-control'}),
         'created_by': forms.HiddenInput(),
         'updated_by': forms.HiddenInput()
      }