from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, get_list_or_404
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



# question types
# 0:select one
# 1:text
# 2:number
# 3:scale
# 4:multiple select