from django import template
import datetime
from micro_blog.models import Post

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_archives(context):
    archives = []
    dates = []
    for each_object in Post.objects.filter(status='P').order_by(
        'published_on'
    ).values('published_on'):
        for date in each_object.values():
            dates.append((date.year, date.month, 1))

    dates = list(set(dates))
    dates.sort(reverse=True)
    for each in dates:
        archives.append(datetime.datetime(each[0], each[1], each[2]))

    if len(archives) > 5:
        return archives[:5]
    return archives


@register.assignment_tag(takes_context=True)
def get_page(context, page, no_pages):
    if page <= 5:
        start_page = 1
    else:
        start_page = page - 5

    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
    if end_page > no_pages:
        end_page = no_pages

    pages = range(start_page, end_page+1)
    return pages


@register.filter
def is_editable_by(post, user):
    return post.is_editable_by(user)


@register.filter
def is_deletable_by(post, user):
    return post.is_deletable_by(user)


@register.filter
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def get_object_list_class(object_list, class_name):
    for c in object_list:
        if c.__class__.__name__ == class_name:
            return True
    return False


@register.filter
def get_slugs(value):
    if value:
        return value.split(',')
    return ''
