from django import template

register = template.Library()


@register.filter(is_safe=True)
def target_blank(a_tag):
    return a_tag.replace('<a ', '<a target="_blank" ')
