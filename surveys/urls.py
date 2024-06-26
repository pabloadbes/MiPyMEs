from django.urls import path
from .views import SurveyListView, SurveyDetailView, SurveyCreate, SurveyUpdate, SurveyDelete, SurveyInitView

surveys_patterns = ([
    path('', SurveyListView.as_view(), name='surveys'),
    path('<int:pk>/<slug:slug>/', SurveyDetailView.as_view(), name='survey'),
    path('create/', SurveyCreate.as_view(), name='create'),
    path('init/<int:pk>', SurveyInitView.as_view(), name='init'),
    path('update/<int:pk>/', SurveyUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', SurveyDelete.as_view(), name='delete')
], 'surveys')