from django import template

register = template.Library()

# Get the last question
@register.filter(name = 'last_question')
def get_last_question(value):
    last_question = value - 1
    return last_question
