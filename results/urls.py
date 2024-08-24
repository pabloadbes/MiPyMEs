from django.urls import path
from . import views

urlpatterns = [
    path('', views.results, name='results'),
    path('<int:result_id>/<slug:result_slug>/', views.result, name='result'),
]