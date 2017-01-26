from django_simple_forum.models import UserProfile
from django.http import HttpResponse


def check_portal_user(view):

    def inner(request, *args, **kwargs):
        if (
            request.user.is_active and
            UserProfile.objects.filter(user=request.user)
        ):
            return HttpResponse("Your don't have access")
        return view(request, *args, **kwargs)

    return inner
