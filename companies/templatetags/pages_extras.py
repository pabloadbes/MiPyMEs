from django import template
from companies.models import Company

register = template.Library()

@register.simple_tag
def get_company_list():
    companies = Company.objects.all()
    return companies