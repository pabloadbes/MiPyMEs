from django import template
from questions.models import Question

register = template.Library()

@register.simple_tag
def get_question_list():
    questions = Question.objects.all()
    return questions