from django import forms
from django_select2 import forms as s2forms
from .models import Survey

class SurveyForm(forms.ModelForm):

   class Meta:
      model = Survey
      fields = ['company', 'survey_type']
      widgets = {
         'company': s2forms.ModelSelect2Widget(
                search_fields=['name__icontains', 'cuit__icontains'],
                attrs={'class': 'form-control'}
            ),
         'survey_type': forms.Select(attrs={'class':'form-control'}),
         'created_by': forms.HiddenInput(),
         'updated_by': forms.HiddenInput()
      }

