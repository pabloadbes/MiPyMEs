from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):

   class Meta:
      model = Survey
      fields = ['company', 'survey_type']
      widgets = {
         'company': forms.Select(attrs={'class':'form-control'}),
         'survey_type': forms.Select(attrs={'class':'form-control'}),
         'created_by': forms.HiddenInput(),
         'updated_by': forms.HiddenInput()
      }

