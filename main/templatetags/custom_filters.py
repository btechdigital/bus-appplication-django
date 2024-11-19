from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def custom_truncate(value, arg):
    stripped_value = strip_tags(value)
    if len(stripped_value) > arg:
        return stripped_value[:arg] + '...'
    return stripped_value