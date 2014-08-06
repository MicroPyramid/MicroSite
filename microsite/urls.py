from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^portal/', include('microadmin.urls', namespace='microadmin')),
    url(r'^portal/pages/', include('pages.urls', namespace='pages')),
    url(r'^portal/projects/', include('projects.urls', namespace='projects')),
    url(r'^portal/staff/', include('payroll.urls', namespace='payroll')),
    url(r'^portal/kb/', include('microkb.urls', namespace='microkb')),
    url(r'^portal/menu/$','pages.views.menu', name='menu'),
    url(r'^portal/menu/addmenuItem/$','pages.views.addmenuitem', name='addmenuitem'),
)
