from django.urls import path
from . import views

urlpatterns = [
    path('', views.responses, name='responses'),
    path('<int:response_id>/<slug:response_slug>/', views.response, name='response'),
]