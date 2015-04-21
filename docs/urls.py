from django.conf.urls import patterns, url

urlpatterns = patterns('docs.views',

    url(r'^books/$', 'books', name='books'),
    url(r'^create-book/$', 'create_book', name='create_book'),
    url(r'^(?P<slug>[-\w]+)/detail/$','view_book', name='view_book'),
    url(r'^(?P<slug>[-\w]+)/$','view_book_doc', name='view_book_doc'),
    url(r'^(?P<slug>[-\w]+)/edit/$','edit_book', name='edit_book'),
    url(r'^(?P<slug>[-\w]+)/approve/$','approve_book', name='approve_book'),
    url(r'^(?P<slug>[-\w]+)/reject/$','reject_book', name='reject_book'),
    url(r'^(?P<slug>[-\w]+)/delete/$','delete_book', name='delete_book'),
    
    url(r'^(?P<slug>[-\w]+)/topics/$', 'view_book_topics', name='view_book_topics'),
    url(r'^(?P<slug>[-\w]+)/create-topic/$', 'create_topic', name='create_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/$','view_topic', name='view_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/edit/$','edit_topic', name='edit_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/approve/$','approve_topic', name='approve_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/reject/$','reject_topic', name='reject_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/delete/$','delete_topic', name='delete_topic'),
)
