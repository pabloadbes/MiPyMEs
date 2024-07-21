from django.forms import BaseModelForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
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

# class SurveyDetailView(DetailView): DEFINIR SI ES NECESARIA
#     model = Survey

class SurveyCreate(CreateView):
    model = Survey
    form_class = SurveyForm

    # def get_form_kwargs(self) -> dict:
    #     kwargs = super().get_form_kwargs()
    #     user = self.request.user
    #     surveyor = Surveyor.objects.get(user_id = user.id)
    #     print("CREANDO ENCUESTA KWARGS")
    #     print(user.first_name)
    #     print(surveyor)
    #     kwargs['initial']['company'] = Company.objects.filter(surveyor_id = surveyor.id)
    #     print(kwargs)
    #     return kwargs

    def get_form(self, form_class=None) -> Survey:
        form = super().get_form(form_class)
        user = self.request.user
        try:
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
    
class SurveyEndView(TemplateView):
    template_name = 'surveys/survey_end.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(id = context['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("home"))
