from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title':'MiPyMEs'})

class SamplePageView(DetailView):
    template_name = "core/sample.html"