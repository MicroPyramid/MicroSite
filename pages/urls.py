from django.conf.urls import patterns, url

urlpatterns = patterns('pages.views',

    url(r'^page/$', 'pages', name='pages'),
    url(r'^page/new/$', 'new_page', name='new_page'),
    url(r'^page/delete/(?P<pk>[a-zA-Z0-9_-]+)/$', 'delete_page', name='delete_page'),
    url(r'^page/edit/(?P<pk>[a-zA-Z0-9_-]+)/$', 'edit_page', name='edit_page'),
    url(r'^menu/$', 'menu', name='menu'),
    url(r'^menu/new/$','add_menu', name='add_menu'),
    url(r'^menu/delete_menu/(?P<pk>[a-zA-Z0-9_-]+)/$', 'delete_menu', name='delete_menu'),
    url(r'^menu/status/(?P<pk>[a-zA-Z0-9_-]+)/$', 'change_menu_status', name='change_menu_status'),
    url(r'^menu/edit/(?P<pk>[a-zA-Z0-9_-]+)/$', 'edit_menu', name='edit_menu'),

)
