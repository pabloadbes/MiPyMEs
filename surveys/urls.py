from django.urls import path
from .views import SurveyListView, SurveyCreate,  SurveyInitView, SurveyEndView

surveys_patterns = ([
    path('', SurveyListView.as_view(), name='surveys'),
    # path('<int:pk>/<slug:slug>/', SurveyDetailView.as_view(), name='survey'), DEFINIR SI ES NECESARIA
    path('create/', SurveyCreate.as_view(), name='create'),
    path('init/<int:pk>', SurveyInitView.as_view(), name='init'),
    path('end/<int:pk>', SurveyEndView.as_view(), name='end'),
    # path('update/<int:pk>/', SurveyUpdate.as_view(), name='update'), DEFINIR SI ES NECESARIA
    # path('delete/<int:pk>/', SurveyDelete.as_view(), name='delete'), DEFINIR SI ES NECESARIA
], 'surveys')