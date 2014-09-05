from django import template
from datetime import date, datetime

register = template.Library()

@register.filter(name='date_diff')
def date_diff(value):
    """Difference between two datetime.date objects"""
    new_date = datetime.strptime(str(value), '%Y-%m-%d').date()
    delta = new_date - date.today()
    return delta.days
