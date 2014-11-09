from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from micro_admin.forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password
from micro_admin.models import User

@login_required
def change_password(request):
	if request.method == 'POST':
		validate_changepassword = ChangePasswordForm(request.POST)
		if validate_changepassword.is_valid():
			user = request.user
			if not check_password(request.POST['oldpassword'],user.password):
				return HttpResponse(json.dumps({'error':True,'response':{'oldpassword':'Invalid old password'}}))
			if request.POST['newpassword'] != request.POST['retypepassword']:
				return HttpResponse(json.dumps({'error':True,'response':{'newpassword':'New password and ConformPasswords did not match'}}))
			user.set_password(request.POST['newpassword'])
			user.save()
			return HttpResponse(json.dumps({'error':False,'response':'Password changed successfully'}))
		else:
			return HttpResponse(json.dumps({'error':True,'response':validate_changepassword.errors}))
	return render_to_response('admin/user/change-password.html')

@login_required
def users(request):
	users = User.objects.all()
	return render_to_response('admin/user/index.html', {'users': users})


def new_user(request):
	return render_to_response('admin/user/new.html')