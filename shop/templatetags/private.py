from django import template

register = template.Library()

@register.filter(name='private')
def private(obj, attribute):
    return str(obj[attribute])