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
from .models import Survey, Variable
from .forms import SurveyForm
from companies.models import Company
from team.models import Surveyor
from results.models import Result

# from questions.models import Question, Section

# Create your views here.
@method_decorator(login_required, name='dispatch')
class SurveyListView(ListView):
    model = Survey

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        user = self.request.user
        # SI ES ENCUESTADOR SOLO MUESTRO LAS ASIGNADAS, SINO MUESTRO TODAS
        if Surveyor.objects.filter(user_id = user.id).exists():
            filtered_queryset = queryset.filter(created_by = user.id)
            return filtered_queryset
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
        initiated_surveys = Survey.objects.all().values_list('company',flat=True)
        # SI ES ENCUESTADOR SOLO MUESTRO LAS ASIGNADAS, SINO MUESTRO TODAS
        if Surveyor.objects.filter(user_id = user.id).exists():
            surveyor = Surveyor.objects.get(user_id = user.id)
            form.fields['company'].queryset = Company.objects.filter(surveyor_id = surveyor.id).exclude(id__in=initiated_surveys)
        else:
            form.fields['company'].queryset = Company.objects.filter().exclude(id__in=initiated_surveys)
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        survey = self.object    
        if survey.get_progress() == 0:
            survey.set_number_of_questions(survey.calculate_number_of_questions())
            survey.set_next_question(survey.get_first_question())
            survey.save()
        return reverse_lazy("questions:question_detail", kwargs={'pk':survey.get_next_question(), 'survey':survey.id})

@method_decorator(login_required, name='dispatch')   
class SurveyEndView(TemplateView):
    template_name = 'surveys/survey_end.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(id = context['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        print("Recuperar y guardar las variables")
        print(self)
        print(request.user)
        print(args)
        print(kwargs)
        result = Result()
        survey_id = kwargs['pk']
        variables = Variable.objects.all().filter(survey_id = survey_id).order_by('id')
        for variable in variables:
            print(variable)
            print(variable.variable_list)
            print(variable.value)
            setattr(result, str(variable.variable_list), variable.value)
        setattr(result, 'created_by', request.user)
        setattr(result, 'updated_by', request.user)
        setattr(result, 'survey_id', survey_id)
        result.save()
        return HttpResponseRedirect(reverse_lazy("home"))
