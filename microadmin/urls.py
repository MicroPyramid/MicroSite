from django.conf.urls import patterns, include, url

urlpatterns = patterns('microadmin',

    url(r'^$', 'views.index', name='index'),
    url(r'^contacts/$', 'views.contacts', name='contacts'),
    url(r'^jobs/$', 'views.jobs', name='jobs'),
    url(r'^users/$', 'views.users', name='users'),
    url(r'^blog/$' ,'blog.index', name='blogindex'),
    url(r'^blog/new/$', 'blog.new'),
    url(r'^out/$', 'views.out', name='out'),
)
