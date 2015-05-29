from django.conf.urls import patterns, url

urlpatterns = patterns(
    'micro_admin',

    url(r'^$', 'index', name='index'),
    url(r'^clear_cache/$', 'clear_cache', name='clear_cache'),
    url(r'^contacts/$', 'contacts', name='contacts'),
    url(r'^contacts/(?P<pk>[-\w]+)/$', 'delete_contact', name='delete_contact'),
    # url(r'^jobs/$', 'jobs', name='jobs'),
    # url(r'^new-jobs/$', 'new_job', name='new_job'),
    # url(r'^edit-jobs/(?P<pk>[-\w]+)/$', 'edit_job', name='edit_job'),
    url(r'^delete-jobs/(?P<pk>[-\w]+)/$', 'delete_job', name='delete_job'),
    url(r'^users/change-state/(?P<pk>\w{0,})/$', 'change_state', name='change_state'),
    url(r'^users/edit/(?P<pk>\w{0,})/$', 'edit_user', name='edit_user'),
    url(r'^out/$', 'out', name='out'),
    url(r'^users/$', 'users', name='users'),
    url(r'^users/new/$', 'new_user', name='new_user'),
    url(r'^users/blogposts/(?P<pk>[a-zA-Z0-9_-]+)/$', 'blogposts', name='blogposts'),
    url(r'^users/reports/(?P<pk>[a-zA-Z0-9_-]+)/$', 'reports', name='reports'),
    url(r'^users/(?P<pk>[a-zA-Z0-9_-]+)/$', 'user_info', name='user_info'),
    url(r'^content/menu/(?P<pk>\w{0,})/order/$', 'menu_order', name='order'),
    url(r'^user/change-password/$', 'change_password', name='change_password'),
)
