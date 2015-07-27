import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):
	sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))[:5]
	suggestions = [{
					'title': result.object.title,
					'link': result.object.get_url,
					'Auther': result.object.user.username,
					'created': str(result.object.updated_on),
					} for result in sqs]
	the_data = json.dumps({
		'results': suggestions
	})
	return HttpResponse(the_data, content_type='application/json')
