"""
Custom template filters for Adabiyya Smart Connect
"""
from django import template

register = template.Library()


@register.filter(name='getattr')
def getattr_filter(obj, attr_name):
    """Get attribute from object, with fallback to getattr."""
    try:
        return getattr(obj, attr_name, '')
    except (AttributeError, TypeError):
        return ''


@register.filter(name='add_class')
def add_class(value, css_class):
    """Add CSS class to form field."""
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': css_class})
    return value


@register.filter(name='attr')
def attr_filter(value, attr_string):
    """Add attributes to form field (format: 'key:value,key2:value2')."""
    if hasattr(value, 'as_widget'):
        attrs = {}
        for pair in attr_string.split(','):
            if ':' in pair:
                key, val = pair.split(':', 1)
                attrs[key.strip()] = val.strip()
        return value.as_widget(attrs=attrs)
    return value


