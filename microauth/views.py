from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
import json


@csrf_protect
def index(request):
	if request.user.is_authenticated():
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
    	return render_to_response('site/login.html',data)


def out(request):
	if not request.user.is_authenticated():
		return HttpResponse('')

	logout(request)
	return HttpResponseRedirect('/')
def permission(request):
	permission = Permission.objects.get(codename='change_content'.name='changecontent')
    user.User_permissions.add(permission)
    if request.User.user_roles=='Admin':
		if request.User.has_perm(microauth.blog_moderator_User):
			return HttpResponse('moderator')
		elif request.User.has_perm(microauth.blogger_User):
			return HttpResponse('BLOGGER')
		elif request.User.has_perm(microauth.can write bllog posts_User):
			return HttpResponse('POSTS')
		elif request.User.has_perm(microauth.can enable or disable blog posts_User):
			return HttpResponse('super')
	elif request.User.user_roles=='Employee':
				