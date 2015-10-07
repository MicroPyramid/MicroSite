from django.conf import settings

class RequestSessionMiddleware(object):
	def process_request(self, request):
		request.session['google_analytics_code'] = settings.GOOGLE_ANALYTICS_CODE
