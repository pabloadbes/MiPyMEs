# from typing import Any, Mapping
from django import forms
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from .models import Company

class CompanyForm(forms.ModelForm):

   class Meta:
      model = Company
      fields = ['name', 'cuit', 'activity_code', 'supervisor', 'year', 'due_id', 'inactive', 'original_id', 'address_street', 'address_number', 'floor', 'sector', 'dept', 'city', 'zip_code', 'phone', 'email', 'web_page']
      widgets = {
         'name': forms.TextInput(attrs={'class':'form-control'}),
         'cuit': forms.TextInput(attrs={'class':'form-control'}),
         'activity_code': forms.NumberInput(attrs={'class':'form-control'}),
         'supervisor': forms.Select(attrs={'class':'form-control'}),
         'year': forms.NumberInput(attrs={'class':'form-control'}), 
         'due_id': forms.NumberInput(attrs={'class':'form-control'}), 
         'inactive': forms.CheckboxInput(), 
         'original_id': forms.NumberInput(attrs={'class':'form-control'}),
         'address_street': forms.TextInput(attrs={'class':'form-control'}),
         'address_number': forms.TextInput(attrs={'class':'form-control'}),
         'floor': forms.NumberInput(attrs={'class':'form-control'}), 
         'sector':forms.TextInput(attrs={'class':'form-control'}), 
         'dept':forms.TextInput(attrs={'class':'form-control'}),
         'city': forms.TextInput(attrs={'class':'form-control'}),
         'zip_code': forms.NumberInput(attrs={'class':'form-control'}),
         'phone': forms.TextInput(attrs={'class':'form-control'}),
         'email': forms.TextInput(attrs={'class':'form-control'}),
         'web_page':forms.TextInput(attrs={'class':'form-control'}),
         'created_by': forms.HiddenInput(),
         'updated_by': forms.HiddenInput()
      }