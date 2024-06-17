from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Company
from .forms import CompanyForm

# Create your views here.
class CompanyListView(ListView):
    model = Company
# def companies(request):
#     # distinct = Response.objects.values('company_id').annotate(companies_count=Count('company_id')).filter(companies_count=1)
#     #responses = Response.objects.values('company_id').annotate(n=Count('pk'))
#     #responses = Response.objects.filter(company_id__in=[item['company_id'] for item in distinct])
#     companies = get_list_or_404(Company)
#     # print(distinct.raw())
#     #print(distinct.__len__())
#     #print(distinct.__str__())
#     print(companies.__len__())
#     print(companies.__str__())
#     # for item in responses:
#     #     company_id = item['company_id']
#     #     print(company_id)
#     #     company = Company.objects.filter(pk=company_id)
#     #     print(company.count())
#     #     print(company.__str__())
#     return render(request, 'companies/companies.html', {'companies':companies})
#     #return render(request, 'responses/responses.html')

class CompanyDetailView(DetailView):
    model = Company
# def company(request, company_id, company_slug):
#     company = get_object_or_404(Company, id=company_id)
#     return render(request, 'companies/company.html', {'company':company})

class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('companies:companies')

class CompanyUpdate(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name_suffix = '_update_form'

    def get_success_url(self) -> str:
        return reverse_lazy('companies:update', args=[self.object.id]) + '?ok'
    
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('companies:companies')