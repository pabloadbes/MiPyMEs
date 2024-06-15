from django.urls import path
from .views import SurveyListView, SurveyDetailView, SurveyCreate

surveys_patterns = ([
    path('', SurveyListView.as_view(), name='surveys'),
    path('<int:pk>/<slug:slug>/', SurveyDetailView.as_view(), name='survey'),
    path('create/', SurveyCreate.as_view(), name='create')
], 'surveys')