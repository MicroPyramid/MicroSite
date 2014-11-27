from django.conf.urls import patterns, include, url

urlpatterns = patterns('micro_admin',

    url(r'^$', 'views.index', name='index'),
    url(r'^contacts/$', 'views.contacts', name='contacts'),
    url(r'^jobs/$', 'views.jobs', name='jobs'),

    url(r'^users/change-state/(?P<pk>\w{0,})/$', 'change_state', name='change_state'),
    url(r'^users/edit/(?P<pk>\w{0,})/$', 'edit_user', name='edit_user'),
    url(r'^out/$', 'views.out', name='out'),

    url(r'^users/$', 'users', name='users'),
    url(r'^users/new/$', 'new_user', name='new_user'),

    url(r'^user/change-password/$', 'change_password', name='change_password'),
)
