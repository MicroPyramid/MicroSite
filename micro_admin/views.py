import json
import string
import random
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models.aggregates import Max
from django.core.exceptions import ObjectDoesNotExist
import sendgrid
from django.core.cache import cache
from micro_admin.models import User
from microsite.settings import SG_USER, SG_PWD
from pages.models import simplecontact, Menu


def index(request):
    if request.user.is_authenticated():
        return render_to_response('admin/index.html', context_instance=RequestContext(request))
    if request.method == "POST":
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'error': False}
            else:
                data = {'error': True, 'message': "The password is valid, but the account has been disabled!"}
        else:
            data = {'error': True, 'message': "The username and password are incorrect."}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        return render_to_response('admin/login.html', context_instance=RequestContext(request))


def out(request):
    if not request.user.is_authenticated():
        return HttpResponse('')

    logout(request)
    return HttpResponseRedirect('/portal/')


@login_required
def contacts(request):
    if not request.user.is_superuser:
        return render_to_response('admin/accessdenied.html')
    contacts = simplecontact.objects.all()
    return render(request, 'admin/content/contacts/simplecontact.html', {'contacts': contacts})


@login_required
def delete_contact(request, pk):
    contact = simplecontact.objects.get(pk=pk)
    if request.user.is_superuser:
        contact.delete()
        data = {'error': False, 'response': 'contact deleted successfully'}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def clear_cache(request):
    cache._cache.flush_all()
    return HttpResponseRedirect('/portal/')


@login_required
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
                    down_link = Menu.objects.get(parent=link_parent, lvl=curr_link.lvl+1)
                    curr_link.lvl = curr_link.lvl+1
                    down_link.lvl = down_link.lvl-1
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
                    up_link = Menu.objects.get(parent=link_parent, lvl=curr_link.lvl-1)
                    curr_link.lvl = curr_link.lvl-1
                    up_link.lvl = up_link.lvl+1
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

            message = "<p><b>Hello "+user.first_name+",</b></p><p>We got a request to reset your password.</p>"
            message += "<p>Here is your new password: "+ pwd_token +"</p>"

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
