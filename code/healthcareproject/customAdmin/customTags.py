# Create a custom_template_tags.py file in your app
from django import template

register = template.Library()

@register.filter
def increment(value):
    return value + 1
