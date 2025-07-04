from django import template

register = template.Library()

@register.filter(name='split')
def split(value, separator):
    """Split a string by separator"""
    if not value:
        return []
    return value.split(separator)

@register.filter(name='strip')
def strip(value):
    """Strip whitespace from a string"""
    if not value:
        return value
    return value.strip()
