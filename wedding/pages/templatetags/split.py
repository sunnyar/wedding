from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='split')
@stringfilter
def split(value):
    """Removes ':' from the given string"""
    value_dict = {}
    value_list = value.split(':')
    value_dict['%s' % (value_list[0])] = '%s' % (value_list[1])
    return value_dict.items()
