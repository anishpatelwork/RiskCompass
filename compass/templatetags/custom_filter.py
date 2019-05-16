""" The custom filters of the app. """
from django import template

register = template.Library()

# Get the last question
@register.filter(name='last_question')
def get_last_question(value):
    """ Returns the id of the question before. """
    last_question = value - 1
    return last_question
