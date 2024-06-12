from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Count
from .models import Response, Company

# Create your views here.
def responses(request):
    # distinct = Response.objects.values('company_id').annotate(companies_count=Count('company_id')).filter(companies_count=1)
    #responses = Response.objects.values('company_id').annotate(n=Count('pk'))
    #responses = Response.objects.filter(company_id__in=[item['company_id'] for item in distinct])
    responses = get_list_or_404(Response)
    # print(distinct.raw())
    #print(distinct.__len__())
    #print(distinct.__str__())
    print(responses.__len__())
    print(responses.__str__())
    # for item in responses:
    #     company_id = item['company_id']
    #     print(company_id)
    #     company = Company.objects.filter(pk=company_id)
    #     print(company.count())
    #     print(company.__str__())
    return render(request, 'responses/responses.html', {'responses':responses})
    #return render(request, 'responses/responses.html')

def response(request, response_id, response_slug):
    response = get_object_or_404(Response, id=response_id)
    return render(request, 'responses/response.html', {'response':response})