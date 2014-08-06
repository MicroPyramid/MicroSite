from django.conf.urls import patterns, include, url

urlpatterns = patterns('pages',

    url(r'^$', 'views.pages', name='pages'),
    url(r'^newpage/$', 'views.new', name='new'),
)
