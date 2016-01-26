import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):
    sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))[:5]
    suggestions = [{
        'title': result.title,
        'link': result.post_url,
        'Auther': result.auther,
        'created': str(result.created_on),
    } for result in sqs]
    the_data = json.dumps({'results': suggestions})
    return HttpResponse(the_data, content_type='application/json')
