from django.template import Library
from docutils.core import publish_string

register = Library()


@register.filter
def is_admin(user):
    if user.is_superuser or user.is_admin:
        return True

@register.filter
def convert_to_html(value):
    return publish_string(value, writer_name='html')