"""Log in to Django without providing a password."""

from django.contrib.auth.backends import ModelBackend
from micro_admin.models import User


class PasswordlessAuthBackend(ModelBackend):

    """Custom authentication in djnago without providing a password."""

    def authenticate(self, username=None):
        try:
            return User.objects.get(email=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
