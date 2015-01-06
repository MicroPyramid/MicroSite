# pylint: disable=W0613,E1120,E1123,E1101
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import RequestContext
import json
from micro_admin.models import User, career
from micro_admin.forms import ChangePasswordForm, CareerForm
from microsite.settings import BLOG_IMAGES
from micro_blog.views import store_image
import os
from pages.models import simplecontact

#@csrf_protect
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
        return render_to_response('admin/login.html',data,context_instance=RequestContext(request))


def out(request):
    if not request.user.is_authenticated():
        return HttpResponse('')

    logout(request)
    return HttpResponseRedirect('/portal/')


@login_required
def contacts(request):
    contacts=simplecontact.objects.all()
    return render_to_response('admin/content/contacts/simplecontact.html',{'contacts':contacts})


@login_required
def jobs(request):
    jobs=career.objects.all()
    return render_to_response('admin/content/jobs/job_list.html',{'jobs':jobs})

@login_required
def new_job(request):
    if request.method=="POST":
        validate_blogcareer=CareerForm(request.POST)
        if validate_blogcareer.is_valid():
            validate_blogcareer = validate_blogcareer.save(commit=False)
            if 'featured_image' in request.FILES:
                validate_blogcareer.featured_image=store_image(request.FILES.get('featured_image'),BLOG_IMAGES)
            else:
                validate_blogcareer.featured_image=''
            validate_blogcareer.save()
            data={'error':False,'response':'jobs are created'}
        else:
            data={'error':True,'response':validate_blogcareer.errors}
        return HttpResponse(json.dumps(data))
    else:
        c={}
        c.update(csrf(request))
        return render_to_response('admin/content/jobs/job.html',{'jobs':jobs,'csrf_token':c['csrf_token']})

@login_required
def edit_job(request,career_slug):
    if request.method=="POST":
        current_careers=career.objects.get(slug=career_slug)
        validate_blogcareer=CareerForm(request.POST,instance=current_careers)
        if validate_blogcareer.is_valid():
            validate_blogcareer = validate_blogcareer.save(commit=False)
            if 'featured_image' in request.FILES:
                if current_careers.featured_image:
                    os.remove(BLOG_IMAGES + current_careers.featured_image)
                validate_blogcareer.featured_image=store_image(request.FILES.get('featured_image'),BLOG_IMAGES)
            else:
                validate_blogcareer.featured_image=''
            validate_blogcareer.save()
            data={'error':False,'response':'job updated successfully'}
        else:
            data={'error':True,'response':validate_blogcareer.errors}
        return HttpResponse(json.dumps(data))
    else:
        blog_career=career.objects.get(slug=career_slug)
        c={}
        c.update(csrf(request))
        return render_to_response('admin/content/jobs/job_edit.html',{'blog_career':blog_career,'csrf_token':c['csrf_token']})


@login_required
def delete_job(request,career_slug):
    careers=career.objects.get(slug=career_slug)
    careers.delete()
    return HttpResponseRedirect('/portal/jobs/')


@login_required
def job_state(request, pk):
    job = career.objects.get(pk=pk)
    if job.is_active:
        job.is_active = False
    else:
        job.is_active = True

    job.save()
    return HttpResponseRedirect('/portal/jobs/')
