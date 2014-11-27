from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'microsite_front.views.index'),
    url(r'^portal/', include('micro_admin.urls', namespace='micro_admin')),
    url(r'^blog/', include('micro_blog.urls', namespace='micro_blog')),
    url(r'^portal/content/', include('pages.urls', namespace='pages')),
    url(r'^portal/projects/', include('projects.urls', namespace='projects')),
    url(r'^portal/staff/', include('payroll.urls', namespace='payroll')),
    url(r'^portal/kb/', include('micro_kb.urls', namespace='micro_kb')),

    url(r'^rss.xml$', 'microsite_front.xml.rss' ),
    url(r'^sitemap.xml$', 'microsite_front.xml.sitemap'),
)
