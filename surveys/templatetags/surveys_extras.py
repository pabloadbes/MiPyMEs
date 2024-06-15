from django import template
from surveys.models import Survey

register = template.Library()

@register.simple_tag
def get_survey_list():
    surveys = Survey.objects.all()
    return surveys