from django.conf.urls import patterns, include, url

urlpatterns = patterns('micro_admin',

    url(r'^$', 'views.index', name='index'),
    url(r'^user/change-password/$', 'views.change_password', name='change_password'),
    url(r'^contacts/$', 'views.contacts', name='contacts'),
    url(r'^jobs/$', 'views.jobs', name='jobs'),
    url(r'^users/$', 'views.users', name='users'),
    url(r'^users/add-new/$', 'views.new_user', name='new_user'),
    url(r'^users/change-state/(?P<pk>\w{0,})/$', 'views.change_state', name='change_state'),
    url(r'^users/delete/(?P<pk>\w{0,})/$', 'views.delete_user', name='delete_user'),
    url(r'^users/edit/(?P<pk>\w{0,})/$', 'views.edit_user', name='edit_user'),
    url(r'^out/$', 'views.out', name='out'),
)
