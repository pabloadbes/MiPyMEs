from django import template
from responses.models import Response

register = template.Library()

@register.simple_tag
def get_response_list():
    responses = Response.objects.all()
    return responses