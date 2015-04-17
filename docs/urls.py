from django.conf.urls import patterns, url

urlpatterns = patterns('docs.views',

    url(r'^books/$', 'books', name='books'),
    url(r'^create-book/$', 'create_book', name='create_book'),
    url(r'^(?P<slug>[-\w]+)/$','view_book', name='view_book'),
    url(r'^(?P<slug>[-\w]+)/topics/$', 'view_book_topics', name='view_book_topics'),
    url(r'^(?P<slug>[-\w]+)/create-topic/$', 'create_topic', name='create_topic'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<topic_slug>[-\w]+)/$','view_topic', name='view_topic'),
)
