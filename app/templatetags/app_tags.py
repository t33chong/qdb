from django import template

register = template.Library()


@register.filter
def target_blank(a_tag):
    return a_tag.replace('<a ', '<a target="_blank" ')
