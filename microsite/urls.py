from django.conf.urls import include, url
from django.conf import settings
from micro_blog.views import report, contact
import micro_blog
from pages.views import site_page
from microsite_front.xml import rss, blog_rss, sitemap
from microsite_front.views import (index, tools, url_checker_tool, s3_objects_set_metadata, career_page,
                                   html_sitemap, page_web_development, page_testing, page_crm,
                                   page_server_maintenance)
from search.views import autocomplete

urlpatterns = [
    url(r'^$', index),
    url(r'^tools/$', tools, name='tools'),
    url(r'^tools/url-checker/$', url_checker_tool,
                                                name='url_checker_tool'),
    url(r'^tools/set-meta-data-for-S3-objects/$', s3_objects_set_metadata,
                                                name='s3_objects_set_metadata'),
    url(r'^report/$', report),
    url(r'^contact-us/$', contact),

    # static pages
    url(r'^web-development/$', page_web_development),
    url(r'^testing/$', page_testing),
    url(r'^crm/$', page_crm),
    url(r'^careers/$', career_page),
    url(r'^server-maintenance/$', page_server_maintenance),

    url(r'^portal/', include('micro_admin.urls', namespace='micro_admin')),
    url(r'^blog/', include('micro_blog.urls', namespace='micro_blog')),
    url(r'^portal/content/', include('pages.urls', namespace='pages')),
    url(r'^portal/employee/', include('employee.urls', namespace='employee')),
    url(r'^books/', include('books.urls', namespace='books')),
    url(r'^sitemap/$', html_sitemap),
    url(r'^(?P<slug>[-\w]+)/$', site_page),
    url(r'^rss.xml$', rss),
    url(r'^blog.rss$', blog_rss),
    url(r'^sitemap.xml$', sitemap),
    url(r'^search/autocomplete/$', autocomplete),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404$', micro_blog.views.handler404),
        url(r'^500$', micro_blog.views.handler500),
    ]
