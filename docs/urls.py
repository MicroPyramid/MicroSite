from django.conf.urls import patterns, url

urlpatterns = patterns('docs.views',

    url(r'^books/$', 'books', name='books'),
    url(r'^books/create-book/$', 'create_book', name='create_book'),
)
