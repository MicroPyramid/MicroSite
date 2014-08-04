from django.conf.urls import patterns, include, url

urlpatterns = patterns('microadmin',

    url(r'^$', 'views.index', name='index'),
    url(r'^blog/$' ,'blog.index', name='blogindex'),
    url(r'^blog/new/$', 'blog.new'),
    url(r'^out/$', 'views.out'),
)
