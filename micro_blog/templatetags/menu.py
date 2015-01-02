from django import template
from micro_blog.models import *
from pages.models import *

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_tags(context):
	return Tags.objects.all().order_by('-id')[:20]


@register.assignment_tag(takes_context=True)
def get_categories(context):
   return Category.objects.all()

@register.assignment_tag(takes_context=True)
def get_latest_posts(context):
   return Post.objects.filter(status='P').order_by('-created_on')[:10]

@register.assignment_tag(takes_context=True)
def get_menus(context):
   return Menu.objects.filter(parent = None).order_by('lvl')
