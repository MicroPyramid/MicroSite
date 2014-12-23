from django.shortcuts import render_to_response
from pages.models import Menu,simplecontact
from micro_blog.models import Tags, Post
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.http.response import HttpResponse
import json
import os
from pages.forms import ContactForm
import datetime
from micro_admin.models import career

def index(request):
	if request.method=="GET":
		menu_list = Menu.objects.filter(parent = None).order_by('lvl')
		tags = Tags.objects.all().order_by('-id')[:20]
		latest_posts = Post.objects.filter(status='P').order_by('created_on')[:5]
		latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
		c = {}
		c.update(csrf(request))
		return render_to_response('site/index.html',{'menu_list':menu_list, 'tags': tags, 'latest_posts':latest_posts, 'latest_featured_posts':latest_featured_posts,'csrf_token':c['csrf_token']})

	else:
		validate_contact=ContactForm(request.POST)
		if validate_contact.is_valid:
			contacts=validate_contact.save()
			try:
				send_mail(contacts.full_name,contacts.message,contacts.email,[contacts.email,'hello@micropyramid.com'],fail_silently=False)
				
				return HttpResponse(json.dumps({"data": 'Thank you,  For Ur Message.!', "error": False}))
			except Exception:
			 	return HttpResponse(json.dumps({"data": 'Server Error.!', "error": False}))

		else:
			for k in validate_contact.errors:
				errors[k] = validate_contact.errors[k][0]
		return HttpResponse(json.dumps(errors))

def career_page(request):
	jobs=career.objects.all()
	menu_list=Menu.objects.filter(parent=None).order_by('lvl')
	tags=Tags.objects.all().order_by('-id')[:20]
	latest_posts=Post.objects.filter(status='P').order_by('created_on')[:5]
	print latest_posts
	return render_to_response('site/careers.html',{'menu_list':menu_list, 'tags': tags,'latest_posts':latest_posts,'jobs':jobs})


	


