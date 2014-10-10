from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^portal/', include('micro_admin.urls', namespace='micro_admin')),
    url(r'^portal/blog/', include('micro_blog.urls', namespace='micro_blog')),
    url(r'^portal/pages/', include('pages.urls', namespace='pages')),
    url(r'^portal/projects/', include('projects.urls', namespace='projects')),
    url(r'^portal/staff/', include('payroll.urls', namespace='payroll')),
    url(r'^portal/kb/', include('micro_kb.urls', namespace='micro_kb')),
    url(r'^portal/menu/$','pages.views.menu', name='menu'),
    url(r'^portal/menu/add_menu_item/$','pages.views.add_menu_item', name='add_menu_item'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'pages.views.delete_menu', name='delete_menu'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/status/$', 'pages.views.status_menu', name='status_menu'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'pages.views.edit_menu', name='edit_menu'),
)
