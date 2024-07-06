from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Question
from surveys.models import Survey, Response
from questions.processors import ctx_dict

# Create your views here.
class QuestionsListView(ListView):
    model = Question

class QuestionDetail(TemplateView):
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id = context['pk'])
        return context

    def post(self, request, *args, **kwargs):
        responses = []
        print("EN EL POST")
        context = self.get_context_data(**kwargs)
        survey_id = context['survey']
        survey = Survey.objects.get(pk = survey_id)
        survey.progress = survey.progress + 1

        ctx = ctx_dict(request)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        print(ctx)
        print(request)
        print("DATA")
        print(data)

        try:
            with transaction.atomic():
                for d in data:
                    response = Response.objects.create(value = data[d], option_id = d, survey_id = survey.id)
                    response.save()
                survey.save()

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponseRedirect(reverse_lazy(""))


        return HttpResponseRedirect(reverse_lazy("questions:question_detail", kwargs={'pk':survey.progress, 'survey':survey.id}))


# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select
