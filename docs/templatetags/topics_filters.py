from django import template
from docs.models import Topic

register = template.Library()

@register.filter
def get_sub_topics(topic):
    sub_topics = Topic.objects.filter(parent = topic)
    return sub_topics
