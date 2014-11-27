from django.template import Library
from micro_admin.models import User

register = Library()


@register.filter
def is_admin(user):
    if user.is_admin:
        return True