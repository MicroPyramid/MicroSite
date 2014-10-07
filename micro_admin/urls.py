from django.conf.urls import patterns, include, url

urlpatterns = patterns('micro_admin',

    url(r'^$', 'views.index', name='index'),
    url(r'^contacts/$', 'views.contacts', name='contacts'),
    url(r'^jobs/$', 'views.jobs', name='jobs'),
    url(r'^users/$', 'views.users', name='users'),
    url(r'^out/$', 'views.out', name='out'),
)
