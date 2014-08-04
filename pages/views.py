from django.shortcuts import render_to_response

# Create your views here.
def page_details(request, slug):
	
	return render_to_response('site/page.html')