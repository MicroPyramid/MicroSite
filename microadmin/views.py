from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
import json
from microsite.settings import BASE_DIR


#@csrf_protect
def index(request):
	if request.user.is_authenticated():
		print 'x'
		return render_to_response('admin/index.html')
	if request.method=="POST":
		user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				login(request, user)
				data = {'error':False}
			else:
				data = {'error':True,'message':"The password is valid, but the account has been disabled!"}
		else:
			data = {'error':True,'message':"The username and password were incorrect."}
		return HttpResponse(json.dumps(data))
	else:
	    	data = {}
	    	data.update(csrf(request))
	    	return render_to_response('admin/login.html',data)


def out(request):
	if not request.user.is_authenticated():
		return HttpResponse('')

	logout(request)
	return HttpResponseRedirect('/portal/')
