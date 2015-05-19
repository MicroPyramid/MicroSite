from django import template
from books.models import Topic

register = template.Library()


@register.filter
def get_sub_topics(topic):
    sub_topics = Topic.objects.filter(parent=topic, shadow__isnull=True)
    return sub_topics
