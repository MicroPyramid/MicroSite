from django.conf.urls import patterns, include, url

urlpatterns = patterns('pages.views',

    url(r'^page/$', 'pages', name='pages'),
    url(r'^page/new/$', 'new_page', name='new_page'),
    url(r'^page/(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'delete_page', name='delete_page'),
    url(r'^page/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'edit_page', name='edit_page'),
    
    url(r'^menu/$', 'menu', name='menu'),
    url(r'^menu/add_menu_item/$','add_menu', name='add_menu'),
    url(r'^menu/(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'delete_menu', name='delete_menu'),
    url(r'^menu/(?P<pk>[a-zA-Z0-9_-]+)/status/$', 'change_menu_status', name='change_menu_status'),
    url(r'^menu/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'edit_menu', name='edit_menu'),

)
