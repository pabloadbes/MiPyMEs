from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Company
from .forms import CompanyForm

# Create your views here.
class CompanyListView(ListView):
    model = Company

class CompanyDetailView(DetailView):
    model = Company

class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('companies:companies')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class CompanyUpdate(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy('companies:update', args=[self.object.id]) + '?ok'
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('companies:companies')