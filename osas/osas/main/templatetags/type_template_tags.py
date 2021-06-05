from django import template
import random
register = template.Library()


@register.filter
def types(x):
    return type(x)


@register.filter
def length(x):
    return len(x)
