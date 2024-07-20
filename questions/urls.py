from django.urls import path
from .views import QuestionDetail

questions_patterns = ([
    # path('', QuestionsListView.as_view(), name='questions'), DEFINIR SI ES NECESARIA
    path('<int:pk>/<int:survey>/', QuestionDetail.as_view(), name='question_detail'),
], 'questions')