from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.template.context_processors import csrf
import json
from micro_admin.forms import ChangePasswordForm, UserForm
from micro_admin.models import USER_ROLES, User
from micro_blog.models import Post
import datetime


@login_required
def users(request):
    users = User.objects.all().order_by('id')
    return render(request, 'admin/user/index.html', {'users': users})


@login_required
def change_password(request):
    if request.method == 'POST':
        validate_changepassword = ChangePasswordForm(request.POST)
        if validate_changepassword.is_valid():
            user = request.user
            if not check_password(request.POST['oldpassword'], user.password):
                return HttpResponse(json.dumps({'error': True, 'response': {'oldpassword': 'Invalid old password'}}),
                                    content_type='application/json; charset=utf-8')
            if request.POST['newpassword'] != request.POST['retypepassword']:
                return HttpResponse(
                    json.dumps(
                        {
                            'error': True, 'response': {
                                'newpassword': 'New password and ConformPasswords did not match'
                            }
                        }),
                    content_type='application/json; charset=utf-8')

            user.set_password(request.POST['newpassword'])
            user.save()
            return HttpResponse(json.dumps({'error': False, 'response': 'Password changed successfully'}),
                                content_type='application/json; charset=utf-8')
        else:
            return HttpResponse(json.dumps({'error': True, 'response': validate_changepassword.errors}),
                                content_type='application/json; charset=utf-8')
    return render(request, 'admin/user/change_password.html')


@login_required
def new_user(request):
    if request.method == 'POST':
        validate_user = UserForm(request.POST)

        if validate_user.is_valid():
            datestring_format = datetime.datetime.strptime(
                request.POST.get('date_of_birth'), "%m/%d/%Y").strftime("%Y-%m-%d")
            date = datetime.datetime.strptime(datestring_format, "%Y-%m-%d")

            user = User.objects.create_user(
                    username=request.POST.get('first_name'),
                    email=request.POST.get('email'),
                    password=request.POST.get('password')
                )
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.user_roles = request.POST.get('user_roles')
            user.date_of_birth = date
            user.date_joined = datetime.datetime.now()
            user.last_login = datetime.datetime.now()
            user.gplus_url = request.POST.get('gplus_url')
            user.fb_profile = request.POST.get('fb_profile')
            user.tw_profile = request.POST.get('tw_profile')
            user.ln_profile = request.POST.get('ln_profile')
            user.about = request.POST.get('about')
            user.state = request.POST.get('state')
            user.city = request.POST.get('city')
            user.address = request.POST.get('address')
            user.mobile = request.POST.get('mobile')
            user.phones = request.POST.get('phones')
            user.pincode = request.POST.get('pincode')

            if request.POST.get('user_roles') == 'Admin':
                user.is_admin = True
                user.is_superuser = True

            if request.POST.get('google_plus_url', False):
                user.google_plus_url = request.POST.get('google_plus_url')

            if request.POST.get('is_active', False):
                user.is_active = True

            if request.POST.get('is_special', False):
                user.is_special = True

            user.save()
            data = {'error': False, 'response': 'User created successfully.'}
        else:
            data = {'error': True, 'response': validate_user.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        if request.user.is_superuser:
            c = {}
            c.update(csrf(request))
            user_roles = USER_ROLES
            return render(request, 'admin/user/new.html', {'user_roles': user_roles, 'csrf_token': c['csrf_token']})
        else:
            return render(request, 'admin/accessdenied.html')


@login_required
def edit_user(request, pk):
    '''does the corresponding form validation and stores the edited details of administrator'''
    current_user = User.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser or request.user == current_user:
            validate_user = UserForm(request.POST, instance=current_user)
            old_password = current_user.password
            if validate_user.is_valid():
                if old_password != request.POST.get('password'):
                    current_user.set_password(request.POST.get('password'))
                edit_user = validate_user.save(commit=False)
                edit_user.user_roles = request.POST.get('user_roles')
                if request.POST.get('user_roles') == 'Admin':
                    edit_user.is_admin = True
                    edit_user.is_superuser = True

                if request.POST.get('google_plus_url'):
                    edit_user.google_plus_url = request.POST.get('google_plus_url')
                else:
                    edit_user.google_plus_url = ''

                if request.POST.get('fb_profile'):
                    edit_user.fb_profile = request.POST.get('fb_profile')
                else:
                    edit_user.fb_profile = ''

                if request.POST.get('tw_profile'):
                    edit_user.tw_profile = request.POST.get('tw_profile')
                else:
                    edit_user.tw_profile = ''

                if request.POST.get('ln_profile'):
                    edit_user.ln_profile = request.POST.get('ln_profile')
                else:
                    edit_user.ln_profile = ''

                if request.POST.get('is_active', False):
                    edit_user.is_active = True

                if request.POST.get('is_special', False):
                    edit_user.is_special = True

                edit_user.save()

                data = {'error': False, 'message': 'updated successfully'}
            else:
                data = {'error': True, 'message': validate_user.errors}
            return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
        else:
            data = {'error': True, 'error_message': "You Dont have permission to edit."}
            return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        if request.user.is_superuser or request.user == current_user:
            c = {}
            c.update(csrf(request))
            current_user = User.objects.get(pk=pk)
            user_roles = USER_ROLES
            return render(
                request,
                'admin/user/edit.html',
                {
                    'role_list': user_roles, 'edit_user': current_user, 'csrf_token': c['csrf_token']
                })
        else:
            return render(request, 'admin/accessdenied.html')


@login_required
def change_state(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return HttpResponseRedirect("/portal/users/")


@login_required
def user_info(request, pk):
    user = User.objects.get(pk=pk)
    blog_posts = Post.objects.filter(user=user)
    return render(
        request,
        'admin/user/view_userinfo.html',
        {
            'blog_posts': blog_posts, 'user': user
        })


@login_required
def blogposts(request, pk):
    user = User.objects.get(pk=pk)
    blog_posts = Post.objects.filter(user=user)
    return render(request, 'admin/user/blogposts.html', {'user': user, 'blog_posts': blog_posts})

