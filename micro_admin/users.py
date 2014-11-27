from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.hashers import check_password
import json

from micro_admin.forms import ChangePasswordForm, UserForm
from micro_admin.models import USER_ROLES, User


@login_required
def users(request):
    users = User.objects.all()
    return render_to_response('admin/user/index.html', {'users': users})


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
def new_user(request):
    if request.method == 'POST':
        validate_user = UserForm(request.POST)
        if validate_user.is_valid():

            user = User.objects.create_user(email=request.POST.get('email'), password=request.POST.get('password'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.gplus_url = request.POST.get('gplus_url')
            user.user_roles = request.POST.get('user_roles')
            if request.POST.get('user_roles') == 'Admin':
                user.is_admin = True

            if request.POST.get('google_plus_url',False):
                user.google_plus_url = request.POST.get('google_plus_url')

            if request.POST.get('is_active',False):
                user.is_active = True
            else:
                user.is_active = False

            user.save()
            print "user saved"
            data = {'error':False, 'response':'created successfully'}
        else:
            #print "erros" + validate_user.errors
            data = {'error':True, 'response':validate_user.errors}
        return HttpResponse(json.dumps(data))
    else:
        c = {}
        c.update(csrf(request))
        user_roles = USER_ROLES
        return render_to_response('admin/user/new.html',{'user_roles':user_roles,'csrf_token':c['csrf_token']})


@login_required
def edit_user(request,pk):
    '''does the corresponding form validation and stores the edited details of administrator'''
    if request.method == 'POST':
        current_user = User.objects.get(pk = pk)
        validate_user = UserForm(request.POST,instance = current_user)
        old_password = current_user.password
        if validate_user.is_valid():
            if old_password != request.POST.get('password'):
                current_user.set_password(request.POST.get('password'))
            current_user.user_roles = request.POST.get('user_roles')
            if request.POST.get('user_roles') == 'Admin':
                current_user.is_admin = True

            if request.POST.get('google_plus_url',False):
                current_user.google_plus_url = request.POST.get('google_plus_url')

            if request.POST.get('is_active',False):
                current_user.is_active = True
            else:
                current_user.is_active = False

            current_user.save()
            print current_user

            data = {'error':False, 'message':'updated successfully'}
        else:
            data = {'error':True, 'message':validate_user.errors}
        return HttpResponse(json.dumps(data))
    else:
        c = {}
        c.update(csrf(request))
        current_user = User.objects.get(pk = pk)
        user_roles = USER_ROLES
        return render_to_response('admin/user/edit.html',{'role_list':user_roles,'edit_user':current_user,'csrf_token':c['csrf_token']})


@login_required
def change_state(request,pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return HttpResponseRedirect("/portal/users/")
