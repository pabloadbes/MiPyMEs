# from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from .models import Survey
from .forms import SurveyForm
from questions.models import Question, Section

# Create your views here.
class SurveyListView(ListView):
    model = Survey

class SurveyDetailView(DetailView):
    model = Survey

class SurveyCreate(CreateView):
    model = Survey
    form_class = SurveyForm

    def get_success_url(self) -> str:
        if self.object.id:
            return reverse_lazy('surveys:init', args=[self.object.id])
        survey = Survey.objects.get(company_id=self.object.company_id)
        return reverse_lazy('surveys:init', args=[survey.id])

class SurveyUpdate(UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy('surveys:update', args=[self.object.id])+'?ok'

class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('surveys:surveys')

class SurveyInitView(TemplateView):
    template_name = 'surveys/survey_init.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(id = context['pk'])
        return context

    def post(self, request, *args, **kwargs):
        #por ahora solo suponemos caso de éxito
        #falta implementar validaciones
        context = self.get_context_data(**kwargs)
        survey = context['survey']    
        survey.set_number_of_questions(survey.calculate_number_of_questions())
        survey.set_next_question(survey.calculate_next_question())
        survey.set_progress(0)
        survey.save()
        return HttpResponseRedirect(reverse_lazy("questions:question_detail", kwargs={'pk':survey.next_question, 'survey':survey.id}))
    
class SurveyEndView(TemplateView):
    template_name = 'surveys/survey_end.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(id = context['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("home"))
