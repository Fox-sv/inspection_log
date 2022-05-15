from django import template


register = template.Library()

@register.filter
def fileformat(value):
    """Returns the fileformat of the filename given in value"""
    file_format = value.split('.')
    return file_format[1]