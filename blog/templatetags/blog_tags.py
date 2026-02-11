from django import template
from home.models import News

register = template.Library()


@register.filter
def truncate_chars(text, num_chars=30):
    if not text:
        return ""

    text = str(text)
    if len(text) <= num_chars:
        return text

    return text[:num_chars] + "..."
