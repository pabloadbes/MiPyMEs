from django.urls import path
from .views import CompanyListView, CompanyDetailView, CompanyCreate, CompanyUpdate, CompanyDelete

companies_patterns = ([
    path('', CompanyListView.as_view(), name='companies'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company'),
    # path('<int:pk>/<slug:slug>/', CompanyDetailView.as_view(), name='company'),
    path('create/', CompanyCreate.as_view(), name='create'),
    path('update/<int:pk>', CompanyUpdate.as_view(), name='update'),
    path('delete/<int:pk>', CompanyDelete.as_view(), name='delete'),
], 'companies')