from django.shortcuts import render_to_response
from pages.models import Menu
from micro_blog.models import Tags, Post

def index(request):
	menu_list = Menu.objects.filter(parent = None).order_by('lvl')
	tags = {} #Tags.objects.all()
	latest_posts = Post.objects.filter(status='P').order_by('created_on')[:5]
	latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
	return render_to_response('site/index.html',{'menu_list':menu_list, 'tags': tags, 'latest_posts':latest_posts, 'latest_featured_posts':latest_featured_posts})
