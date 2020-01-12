from django import template

register = template.Library()

@register.filter(name='split')
def split(value,arg):
    sp = arg.split(':')[0]
    ind = arg.split(':')[1]
    return value.split(sp)[int(ind)]