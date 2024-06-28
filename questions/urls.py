from django.urls import path
from .views import QuestionsListView, QuestionDetail

questions_patterns = ([
    path('', QuestionsListView.as_view(), name='questions'),
    path('<int:pk>/<slug:slug>/', QuestionDetail.as_view(), name='question_detail'),
    #path('form0/<int:pk>/<slug:slug>/', Question0FormView.as_view(), name='question0_form'),
], 'questions')