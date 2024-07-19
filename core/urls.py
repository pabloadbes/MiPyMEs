from django.urls import path
from .views import HomePageView, RootRedirectView

urlpatterns = [
    path('', RootRedirectView.as_view(), name="root"),
    path('home/', HomePageView.as_view(), name="home"),
    # path('', HomePageView.as_view(), name="home"),
    # path('sample/', SamplePageView.as_view(), name="sample"),
]