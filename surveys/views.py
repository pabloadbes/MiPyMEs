from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Survey
from .forms import SurveyForm

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
        context["survey"] = Survey.objects.all().filter(id = context['pk']).first().__get_survey__()
        print("CONTEXTO DE INIT")
        # print(context)
        # print(context['survey'].survey_type_id)
        # print("SELF DE INIT")
        # print(self)
        # # print(self.name)
        # print(self.__dict__)
        return context
    
    def get(self, request, *args, **kwargs):
        # Lógica para manejar solicitudes GET
        print("TAMO EN EL GET")
        print(self)
        print(request)
        print(args)
        print(kwargs)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print("TAMO EN EL POST")
        print(self)
        print(request)
        print(args)
        print(kwargs)
        # Lógica para manejar solicitudes POST
        # Puedes acceder a los datos del formulario con request.POST
        data = request.POST.get('campo')
        # Procesa los datos del formulario aquí
        context = self.get_context_data(**kwargs)
        context['resultado'] = 'Datos procesados'
        return self.render_to_response(context)
    
# class SurveyInitView(FormView):
#     template_name = 'surveys/survey_init.html'
#     form_class = SurveyForm
#     success_url = 'surveys/surveys.html'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.send_email()
#         return super().form_valid(form)
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["survey"] = Survey.objects.all().filter(id = context['pk']).first().__get_survey__()
#     #     print("CONTEXTO DE INIT")
#     #     print(context)
#     #     print(context['survey'].survey_type_id)
#     #     print("SELF DE INIT")
#     #     print(self)
#     #     # print(self.name)
#     #     print(self.__dict__)
#     #     return context