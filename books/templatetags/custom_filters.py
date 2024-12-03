from django import template

register = template.Library()

@register.filter
def uppercase(value):
    return value.upper()
