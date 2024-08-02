from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Question
from surveys.models import Survey, Response
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
        print("context del get_context_data")
        print(context)
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

        ########################################################
        ########################################################
        ########################################################
        print("EN EL POST")
        print(question)
        question_dict = question.__dict__
        print(question_dict)
        print(ctx)
        print(ctx['items'])
        print(context)
        ########################################################
        ########################################################
        ########################################################

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
