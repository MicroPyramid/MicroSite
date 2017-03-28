import json
import string
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max
from django.core.exceptions import ObjectDoesNotExist
import sendgrid
# from django.core.cache import cache
from micro_admin.models import User
from microsite.settings import SG_USER, SG_PWD
from pages.models import Menu
from micro_blog.models import Post
from datetime import datetime
from datetime import timedelta
import requests
from django.core.urlresolvers import reverse
from django.conf import settings


def is_employee(function):

    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return render(request, 'admin/login.html')
        elif not request.user.is_superuser and not request.user.is_employee:
            raise Http404
        else:
            return function(request, *args, **kw)
    return wrapper



def index(request):
    if request.user.is_authenticated():
        # if not (request.user.is_employee or request.user.is_staff):
        #     raise Http404
        if request.POST.get('timestamp', ""):
            date = request.POST.get('timestamp').split(' - ')
            start_date = datetime.strptime(date[0], "%Y/%m/%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(date[1], "%Y/%m/%d").strftime("%Y-%m-%d")
            post = Post.objects.filter(created_on__range=(start_date, end_date)).values_list('user', flat=True)
            users = User.objects.filter(id__in=post)
        else:
            current_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            previous_date = datetime.strptime(str(datetime.now().date() - timedelta(days=7)), "%Y-%m-%d").strftime("%Y-%m-%d")
            post = Post.objects.filter(created_on__range=(previous_date, current_date)).values_list('user', flat=True)
            users = User.objects.filter(id__in=post)
        return render(request, 'admin/index.html', {'users' : users})
    if request.method == "POST":
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'error': False}
            else:
                data = {'error': True, 'message': "Your account has been disabled!"}
        else:
            data = {'error': True, 'message': "The username and password are incorrect."}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        return render(request, 'admin/login.html')


def out(request):
    if not request.user.is_authenticated():
        return HttpResponse('')

    logout(request)
    return HttpResponseRedirect('/portal/')

# @login_required
# @is_employee
# def clear_cache(request):
#     cache._cache.flush_all()
#     return HttpResponseRedirect('/portal/')


@login_required
@is_employee
def menu_order(request, pk):
    if request.method == 'POST':
        if request.POST.get('mode') == 'down':
            link_parent = Menu.objects.get(pk=pk).parent
            curr_link = Menu.objects.get(pk=pk)
            lvlmax = Menu.objects.filter(parent=pk).aggregate(Max('lvl'))['lvl__max']
            if lvlmax == curr_link.lvl:
                data = {'error': True, 'message': 'You cant move down.'}
            count = Menu.objects.all().count()
            if count == curr_link.lvl:
                data = {'error': True, 'message': 'You cant move down.'}
            else:
                try:
                    down_link = Menu.objects.get(parent=link_parent, lvl=curr_link.lvl + 1)
                    curr_link.lvl = curr_link.lvl + 1
                    down_link.lvl = down_link.lvl - 1
                    curr_link.save()
                    down_link.save()
                except ObjectDoesNotExist:
                    pass
                data = {'error': False}
        else:
            link_parent = Menu.objects.get(pk=pk).parent
            curr_link = Menu.objects.get(pk=pk)
            count = Menu.objects.all().count()
            if curr_link.lvl == 1:
                data = {'error': True, 'message': 'You cant move up.'}
            else:
                try:
                    up_link = Menu.objects.get(parent=link_parent, lvl=curr_link.lvl - 1)
                    curr_link.lvl = curr_link.lvl - 1
                    up_link.lvl = up_link.lvl + 1
                    curr_link.save()
                    up_link.save()
                except ObjectDoesNotExist:
                    pass
                data = {'error': False}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def forgot_password(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get("email"))
            chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
            pwd_token = ''.join(random.choice(chars) for i in range(20))

            user.set_password(pwd_token)
            user.save()

            message = "<p><b>Hello " + user.first_name + ",</b></p><p>We got a request to reset your password.</p>"
            message += "<p>Here is your new password: " + pwd_token + "</p>"

            sg = sendgrid.SendGridClient(SG_USER, SG_PWD)
            sending_msg = sendgrid.Mail()
            sending_msg.set_subject("Reset Your Password")
            sending_msg.set_html(message)
            sending_msg.set_text('Reset Your Password')
            sending_msg.set_from("hello@micropyramid.com")
            sending_msg.add_to(request.POST.get('email'))
            sg.send(sending_msg)

            data = {'error': False, "message": "Password has been sent to your email sucessfully."}

        except ObjectDoesNotExist:
            data = {'error': True, "message": "Entered Email id is incorrect."}

        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def google_login(request):
    if 'code' in request.GET:
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri':  request.scheme + '://' + request.META['HTTP_HOST'] + reverse('micro_admin:google_login'),
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }

        info = requests.post(
            "https://accounts.google.com/o/oauth2/token", data=params)
        info = info.json()
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        params = {'access_token': info['access_token']}
        kw = dict(params=params, headers={}, timeout=60)
        response = requests.request('GET', url, **kw)
        user_document = response.json()
        email_matches = User.objects.filter(email=user_document['email'])
        link = "https://plus.google.com/" + user_document['id']

        if email_matches:
            user = email_matches[0]

            # if not user.is_gp_connected:
            #     Google.objects.create(
            #         user=user,
            #         google_url=link,
            #         verified_email=user_document['verified_email'],
            #         google_id=user_document['id'],
            #         family_name=user_document['family_name'],
            #         name=user_document['name'],
            #         given_name=user_document['given_name'],
            #         dob=dob,
            #         email=user_document['email'],
            #         gender=gender,
            #         picture=picture,
            #     )
            if user.is_active and user.email.split('@')[-1] == 'micropyramid.com':
                user.google_plus_url = link
                user.save()
                user = authenticate(username=user.email)
                login(request, user)
                return HttpResponseRedirect('/portal/')
        return HttpResponseRedirect('/')
    else:
        rty = "https://accounts.google.com/o/oauth2/auth?client_id=" + \
               settings.GP_CLIENT_ID + "&response_type=code"
        rty += "&scope=https://www.googleapis.com/auth/userinfo.profile" + \
            " https://www.googleapis.com/auth/userinfo.email" + \
            " https://www.google.com/m8/feeds/contacts/&redirect_uri=" + \
            request.scheme + '://' + \
            request.META['HTTP_HOST'] + \
            reverse('micro_admin:google_login') + "&state=1235dfghjkf123"
        return HttpResponseRedirect(rty)
