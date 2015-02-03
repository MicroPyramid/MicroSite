from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.http.response import HttpResponse
import json
from pages.forms import ContactForm
from micro_admin.models import career
from memoize import memoize, delete_memoized, delete_memoized_verhash

def index(request):
	if request.method=="GET":
		latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
		c = {}
		c.update(csrf(request))
		return render_to_response('site/index.html',{'latest_featured_posts':latest_featured_posts,'csrf_token':c['csrf_token']})
	else:
		validate_contact=ContactForm(request.POST)
		errors = {}
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
	jobs=career.objects.filter(is_active=True).order_by('created_on')
	return render_to_response('site/careers.html',{'jobs':jobs})

