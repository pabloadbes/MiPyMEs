from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Survey

# Create your views here.
class SurveyListView(ListView):
    model = Survey

class SurveyDetailView(DetailView):
    model = Survey

class SurveyCreate(CreateView):
    model = Survey
    fields = ['company']