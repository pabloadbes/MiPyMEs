from django.urls import path
from .views import QuestionsListView, QuestionDetail

questions_patterns = ([
    path('', QuestionsListView.as_view(), name='questions'),
    path('<int:pk>/<int:survey>/', QuestionDetail.as_view(), name='question_detail'),
], 'questions')