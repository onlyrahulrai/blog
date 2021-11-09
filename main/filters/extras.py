from django import template

register = template.Library()


@register.filter(name="get_val")
def get_val(dict, key):
    return dict.get(key)

@register.simple_tag
def define(val=None):
    if val:
        query = val.replace(" ","+")
        return f"?query={query}&page="
    return "?page="
