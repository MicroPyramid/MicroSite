from django.conf.urls import patterns, include, url

urlpatterns = patterns('pages',

    url(r'^$', 'views.pages', name='pages'),
    url(r'^$', 'views.menu', name='menu'),
    url(r'^newpage/$', 'views.new', name='new'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'views.deletepage', name='deletepage'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/status/$', 'views.statuspage', name='statuspage'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'views.editpage', name='editpage'),
)
