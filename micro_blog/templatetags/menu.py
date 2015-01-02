from django import template
from micro_blog.models import *

register = template.Library()

@register.filter
def menu():
	menu_list = Menu.objects.filter(parent = None).order_by('lvl')
	latest_posts = Post.objects.filter(status='P').order_by('-created_on')[:10]
	categories = Category.objects.all()
	tags = Tags.objects.all().order_by('-id')[:20]
	return menu_list,latest_posts,categories,tags
