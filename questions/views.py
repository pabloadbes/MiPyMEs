from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Question
from surveys.models import Survey, Response, Variable
from companies.models import Company
from team.models import Supervisor, Surveyor
from questions.processors import ctx_dict

# Create your views here.
# class QuestionsListView(ListView): DEFINIR SI ES NECESARIA
#     model = Question

@method_decorator(login_required, name='dispatch')
class QuestionDetail(TemplateView):
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id = context['pk'])
        context["survey_data"] = Survey.objects.get(id = context['survey'])
        surveyor = Company.objects.get(id = context["survey_data"].company.id).surveyor
        context["surveyor_asigned"] = surveyor
        supervisor = Supervisor.objects.get(id = surveyor.supervisor.id)
        context["supervisor"] = supervisor
        context["surveyors"] = Surveyor.objects.all().exclude(id = surveyor.id)
        return context

    def post(self, request, *args, **kwargs):
        user_id = self.request.user
        context = self.get_context_data(**kwargs)
        survey_id = context['survey']
        survey = Survey.objects.get(pk = survey_id)
        question = context['question']

        if survey.is_survey_complete():
            survey.set_survey_state(2)
        survey.set_next_question(survey.calculate_next_question())
        survey.set_progress(100 * question.number / survey.get_number_of_questions())
        survey.set_updated_by(user_id)

        ctx = ctx_dict(request)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        try:
            with transaction.atomic():
                if "text" in ctx['template_type'] or "number" in ctx['template_type'] or "scale" in ctx['template_type']:
                    for d in data:
                        response = Response.objects.create(value = data[d], option_id = d, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                        response.save()
                
                elif "select_one" in ctx['template_type']:
                    for item in ctx['items']:
                        for option in item[1]:
                            if option[0].text == data[str(item[0].id)]:
                                response = Response.objects.create(value = "true", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            else: 
                                response = Response.objects.create(value = "false", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            response.save()

                elif "select_many" in ctx['template_type']: #falta poner a prueba este caso
                    selected_options = data.keys()
                    for item in ctx['items']:
                        for option in item[1]:
                            if str(option[0].id) in selected_options:
                                response = Response.objects.create(value = "true", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            else: 
                                response = Response.objects.create(value = "false", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            response.save()

                elif "init_1" in ctx['template_type']:
                    item = ctx['items'][0]
                    option_encuestador = item[1][1][0]
                    vble_tipo_cuest = item[1][0][2]
                    vble_encuestador = item[1][1][2]
                    vble_supervisor = item[1][2][2]
                    response_encuestador = Response.objects.create(value = data['surveyor'], option_id = option_encuestador.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_tipo_cuest = Variable.objects.create(value = survey.survey_type.id, survey_id = survey.id, variable_list_id = vble_tipo_cuest.id, created_by = user_id, updated_by = user_id)
                    variable_encuestador = Variable.objects.create(value = data['surveyor'], survey_id = survey.id, variable_list_id = vble_encuestador.id, created_by = user_id, updated_by = user_id)
                    variable_supervisor = Variable.objects.create(value = context['supervisor'].SUP_CODE, survey_id = survey.id, variable_list_id = vble_supervisor.id, created_by = user_id, updated_by = user_id)

                    response_encuestador.save()
                    variable_tipo_cuest.save()
                    variable_encuestador.save()
                    variable_supervisor.save()

                elif "init_2" in ctx['template_type']:
                    item_entrevista = ctx['items'][0]
                    item_fecha = ctx['items'][1]
                    option_entrevista = item_entrevista[1][0][0]
                    option_fecha = item_fecha[1][0][0]
                    vble_entrevista = item_entrevista[1][0][2]
                    vble_fecha = item_fecha[1][0][2]
                    response_entrevista = Response.objects.create(value = data['entrevista'], option_id = option_entrevista.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_fecha = Response.objects.create(value = data['fecha'], option_id = option_fecha.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_entrevista = Variable.objects.create(value = data['entrevista'], survey_id = survey.id, variable_list_id = vble_entrevista.id, created_by = user_id, updated_by = user_id)
                    variable_fecha = Variable.objects.create(value = data['fecha'], survey_id = survey.id, variable_list_id = vble_fecha.id, created_by = user_id, updated_by = user_id)

                    response_entrevista.save()
                    response_fecha.save()
                    variable_entrevista.save()
                    variable_fecha.save()

                survey.save()

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponseRedirect(reverse_lazy("home"))

        if question.number == survey.get_number_of_questions():
            return HttpResponseRedirect(reverse_lazy("surveys:end", args=[survey.id]))
        return HttpResponseRedirect(reverse_lazy("questions:question_detail", kwargs={'pk':survey.next_question, 'survey':survey.id}))


# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select
