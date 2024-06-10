from django.urls import path
from . import views

urlpatterns = [
    path('', views.questions, name='questions'),
    path('<int:question_id>/<slug:question_slug>/', views.question, name='question'),
]