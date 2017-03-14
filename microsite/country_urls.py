from django.conf import settings
from .resolvers import CountryRegexURLResolver
from django.core.urlresolvers import get_resolver


def country_patterns(*urls, prefix_default_country=True):
    """
    Adds the country code prefix to every URL pattern within this
    function. This may only be used in the root URLconf, not in an included
    URLconf.
    """
    if not settings.USE_COUNTRY_URL:
        return list(urls)
    return [CountryRegexURLResolver(list(urls), prefix_default_country=prefix_default_country)]


def is_country_prefix_patterns_used(urlconf):

    for url_pattern in get_resolver(urlconf).url_patterns:
        if isinstance(url_pattern, CountryRegexURLResolver):
            return True, url_pattern.prefix_default_country
    return False, False
