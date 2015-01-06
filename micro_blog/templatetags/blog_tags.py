from django import template
import datetime
import math

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_archives(context):
	archives = []
	current_date = datetime.date.today()
	for i in reversed(range(-4,1)):
	    archives.append(current_date + datetime.timedelta(i*365/12))
	return archives

