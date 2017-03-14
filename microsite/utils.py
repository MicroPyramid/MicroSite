import re
from django.conf import settings
from threading import local

COUNTRY_SESSION_KEY = '_country'
country_code_prefix_re = re.compile(r'^/(\w+([@-]\w+)?)(/|$)')


_language_from_path = local()


def set_country_from_thread(language):
    _language_from_path.value = language


def get_country_from_thread():
    return getattr(_language_from_path, 'value', None)


def get_country_from_path(path, strict=False):

    regex_match = country_code_prefix_re.match(path)
    if not regex_match:
        return None
    lang_code = regex_match.group(1)
    return lang_code


def get_country_from_request(request, check_path=False):

    if check_path:
        lang_code = get_country_from_path(request.path_info)
        print ("language_code")
        print (lang_code)
        if lang_code is not None:
            return lang_code

    # if hasattr(request, 'session'):
    #     country_code = request.session.get(COUNTRY_SESSION_KEY)
    #     if country_code:
    #         return country_code

    country_code = request.COOKIES.get(settings.COUNTRY_COOKIE_NAME)

    if not lang_code:
        return settings.COUNTRY_CODE
