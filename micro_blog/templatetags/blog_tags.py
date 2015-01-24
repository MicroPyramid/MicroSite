from django import template
import datetime

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_archives(context):
	archives = []
	current_date = datetime.date.today()
	for i in reversed(range(-4,1)):
	    archives.append(current_date + datetime.timedelta(i*365/12))
	return archives

@register.assignment_tag(takes_context=True)
def get_page(context,page,no_pages):
	if page <= 5:
		start_page = 1
	else:
		start_page = page-5

	if no_pages <= 10:
		end_page = no_pages
	else:
		end_page = start_page + 10
	if end_page > no_pages:
		end_page=no_pages

	pages = range(start_page, end_page+1)
	return pages

@register.filter
def is_editable_by(post,user):
	return post.is_editable_by(user)

@register.filter
def is_deletable_by(post,user):
	return post.is_deletable_by(user)			