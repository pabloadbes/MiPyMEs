from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):

   class Meta:
      model = Survey
      fields = ['company']
      widgets = {
         'company': forms.Select(attrs={'class':'form-control'})
      }