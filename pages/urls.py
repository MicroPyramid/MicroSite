from django.conf.urls import patterns, include, url

urlpatterns = patterns('pages',

    url(r'^$', 'views.pages', name='pages'),
    url(r'^$', 'views.menu', name='menu'),
    url(r'^new/$', 'views.new_page', name='new_page'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'views.delete_page', name='delete_page'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/status/$', 'views.status_page', name='status_page'),
    url(r'^(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'views.edit_page', name='edit_page'),
)
