from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title':'MiPyMEs'})

class HomeRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('home')
   
class RootRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('home')
        else:
            return reverse('login')