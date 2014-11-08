from django.conf.urls import patterns, include, url

urlpatterns = patterns('micro_admin',

    url(r'^$', 'views.index', name='index'),
    url(r'^contacts/$', 'views.contacts', name='contacts'),
    url(r'^jobs/$', 'views.jobs', name='jobs'),
    url(r'^out/$', 'views.out', name='out'),

    url(r'^users/$', 'users.users', name='users'),
    url(r'^users/new$', 'users.new_user', name='new_user'),
    url(r'^user/change-password/$', 'users.change_password', name='change_password'),
)
