from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    
    url(r'^portal/', include('microadmin.urls', namespace='microadmin')),
    url(r'^proposal/blog/', include('blog.urls', namespace='blog')),
    url(r'^portal/pages/', include('pages.urls', namespace='pages')),
    url(r'^portal/projects/', include('projects.urls', namespace='projects')),
    url(r'^portal/staff/', include('payroll.urls', namespace='payroll')),
    url(r'^portal/kb/', include('microkb.urls', namespace='microkb')),
    url(r'^portal/menu/$','pages.views.menu', name='menu'),
    url(r'^portal/menu/addmenuitem/$','pages.views.addmenuitem', name='addmenuitem'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/delete/$', 'pages.views.deletemenu', name='deletemenu'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/status/$', 'pages.views.statusmenu', name='statusmenu'),
    url(r'^portal/menu/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', 'pages.views.editmenu', name='editmenu'),
)
