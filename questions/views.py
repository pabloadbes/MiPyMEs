from typing import Any
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.edit import FormView
from django.shortcuts import render
from .models import Question

# Create your views here.
# def questions(request):
#     questions = get_list_or_404(Question)
#     return render(request, 'questions/questions.html', {'questions':questions})

class QuestionsListView(ListView):
    model = Question

# def question(request, question_id, question_slug):
#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'questions/question.html', {'question':question})

class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        # print(ctx)
        # print("HOLANDA")
        # print("context")
        context = super().get_context_data(**kwargs)
        #context[""] =
        # print(context)
        # print("self")
        # print(self.get_object)
        # items = Item.objects.all().filter(question_id=question.id)
        # print("ITEM")
        # print(items)
        return context


# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select

# Primer intento formulario simple
# class Question0FormView(FormView):
#     model = Question
#     template_name = 'questions/question0.html'
#     form_class = Question0Form
#     success_url = '/'

#     def form_valid(self, form: Question0Form) -> HttpResponse:
#         print("TODO OK CON EL TIPO 0 PREGUNTA")
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         print("self")
#         print(self.model.objects.all())
#         print("kwargs")
#         print(**kwargs)
#         print("dict")
#         print(dict)
#         print("super")
#         print(super().get_context_data(**kwargs))
#         return super().get_context_data(**kwargs)

# Segundo intento formulario con modelo
# Al parecer me sirve solo para CRUD