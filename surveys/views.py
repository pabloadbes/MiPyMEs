# from django.forms import BaseModelForm
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from .models import Survey
from .forms import SurveyForm
from companies.models import Company
from team.models import Surveyor

# from questions.models import Question, Section

# Create your views here.
@method_decorator(login_required, name='dispatch')
class SurveyListView(ListView):
    model = Survey

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        user = self.request.user
        try: # SI ES ENCUESTADOR SOLO MUESTRO LAS ASIGNADAS, SINO MUESTRO TODAS
            surveyor = Surveyor.objects.get(user_id = user.id)
            filtered_queryset = queryset.filter(created_by = surveyor.id)
            return filtered_queryset
        except:
            pass
        return queryset

# class SurveyDetailView(DetailView): DEFINIR SI ES NECESARIA
#     model = Survey

@method_decorator(login_required, name='dispatch')
class SurveyCreate(CreateView):
    model = Survey
    form_class = SurveyForm

    def get_form(self, form_class=None) -> Survey:
        form = super().get_form(form_class)
        user = self.request.user
        try: # SI ES ENCUESTADOR SOLO MUESTRO LAS ASIGNADAS, SINO MUESTRO TODAS
            surveyor = Surveyor.objects.get(user_id = user.id)
            form.fields['company'].queryset = Company.objects.filter(surveyor_id = surveyor.id)
        except:
            pass
        return form
    
    def get_success_url(self) -> str:
        if self.object.id:
            return reverse_lazy('surveys:init', args=[self.object.id])
        survey = Survey.objects.get(company_id=self.object.company_id)
        return reverse_lazy('surveys:init', args=[survey.id])

# class SurveyUpdate(UpdateView): DEFINIR SI ES NECESARIA
#     model = Survey
#     form_class = SurveyForm
#     template_name_suffix = '_update_form'

#     def get_success_url(self) -> str:
#         return reverse_lazy('surveys:update', args=[self.object.id])+'?ok'

# class SurveyDelete(DeleteView): DEFINIR SI ES NECESARIA
#     model = Survey
#     success_url = reverse_lazy('surveys:surveys')

@method_decorator(login_required, name='dispatch')
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
        survey.set_progress(0)
        survey.save()
        return HttpResponseRedirect(reverse_lazy("questions:question_detail", kwargs={'pk':survey.next_question, 'survey':survey.id}))

@method_decorator(login_required, name='dispatch')   
class SurveyEndView(TemplateView):
    template_name = 'surveys/survey_end.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(id = context['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("home"))
