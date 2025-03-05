from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def human_readable_date(value):
    return value.strftime('%A, %B %dth %Y, %H:%M')
