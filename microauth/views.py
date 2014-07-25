from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		return render_to_response('admin/index.html')
	else:
		return render_to_response('admin/login.html')


def out(request):
	return HttpResponseRedirect('/')