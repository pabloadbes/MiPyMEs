from django.urls import path
from .views import QuestionsListView, QuestionDetail

urlpatterns = [
    path('', QuestionsListView.as_view(), name='questions'),
    path('<int:pk>/<slug:slug>/', QuestionDetail.as_view(), name='question'),
]