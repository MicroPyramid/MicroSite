from django.conf.urls import url
from books.views import (book_list, books, create_book, book_info, view_book, edit_book,
                         approve_book, reject_book, delete_book, view_book_topics, create_topic,
                         view_topic, create_content, reject_topic, delete_topic, approve_topic,
                         subtopic_info, topic_info, view_subtopic, change_topic_order)


urlpatterns = [
    url(r'^$', book_list, name='book_list'),
    url(r'^list/$', books, name='books'),
    url(r'^create-book/$', create_book, name='create_book'),
    url(r'^(?P<slug>[-\w]+)/$', book_info, name='book_info'),
    url(r'^(?P<slug>[-\w]+)/detail/$', view_book, name='view_book'),
    # url(r'^(?P<slug>[-\w]+)/$', view_book_doc, name='view_book_doc'),
    url(r'^(?P<slug>[-\w]+)/edit/$', edit_book, name='edit_book'),
    url(r'^(?P<slug>[-\w]+)/approve/$', approve_book, name='approve_book'),
    url(r'^(?P<slug>[-\w]+)/reject/$', reject_book, name='reject_book'),
    url(r'^(?P<slug>[-\w]+)/delete/$', delete_book, name='delete_book'),
    url(r'^(?P<slug>[-\w]+)/topics/$', view_book_topics, name='view_book_topics'),
    url(r'^(?P<slug>[-\w]+)/create-topic/$', create_topic, name='create_topic'),
    url(r'^(?P<book_slug>[-\w]+)/topic/(?P<topic_slug>[-\w]+)/$', view_topic, name='view_topic'),
    # url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/edit/$', edit_topic, name='edit_topic'),
    url(r'^content/(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/$', create_content, name='create_content'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/reject/$', reject_topic, name='reject_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/delete/$', delete_topic, name='delete_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/approve/$', approve_topic, name='approve_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/(?P<subtopic_slug>[-\w]+)/$', subtopic_info, name='subtopic_info'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/$', topic_info, name='topic_info'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/(?P<subtopic_slug>[-\w]+)/view/$', view_subtopic, name='view_subtopic'),
    url(r'^(?P<book_slug>[-\w]+)/change/(?P<topic_slug>[-\w]+)/order/$', change_topic_order, name='change_topic_order'),
]
