from django.shortcuts import render
from micro_admin.models import career

def index(request):
	latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
	return render(request, 'site/index.html', {'latest_featured_posts': latest_featured_posts})


def career_page(request):
	jobs = career.objects.filter(is_active=True).order_by('created_on')
	return render(request, 'site/careers.html', {'jobs': jobs})

