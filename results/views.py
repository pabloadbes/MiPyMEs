from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Result

# Create your views here.
def results(request):
    results = get_list_or_404(Result)
    return render(request, 'results/results.html', {'results':results})

def result(request, result_id, result_slug):
    result = get_object_or_404(Result, id=result_id)
    return render(request, 'results/result.html', {'result':result})