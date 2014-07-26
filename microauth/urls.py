from django.conf.urls import patterns, include, url

urlpatterns = patterns('microauth.views',

    url(r'^$', 'index'),
    url(r'^out/$', 'out'),
)
