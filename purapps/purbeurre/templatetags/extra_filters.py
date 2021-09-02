"""Extra filters for template."""
from django import template

register = template.Library()


@register.filter(name="get_strings_before_comma")
def get_strings_before_comma(value):
    """Get strings before the first comma."""
    return value[: value.find(",")] if value.find(",") > 0 else value
