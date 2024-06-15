from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Survey

# Create your views here.
class SurveyListView(ListView):
    model = Survey

class SurveyDetailView(DetailView):
    model = Survey

class SurveyCreate(CreateView):
    model = Survey
    fields = ['company']
    success_url = reverse_lazy('surveys:surveys')
    # debo redirigir a continuar llenando encuesta

class SurveyUpdate(UpdateView):
    model = Survey
    fields = ['company']
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy('surveys:update', args=[self.object.id])+'?ok'

class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('surveys:surveys')