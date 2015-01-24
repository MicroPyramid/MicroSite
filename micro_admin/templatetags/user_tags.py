from django.template import Library

register = Library()


@register.filter
def is_admin(user):
    if user.is_admin:
        return True