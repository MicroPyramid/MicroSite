from django.conf.urls import include, url
from django.conf import settings

from django.contrib import admin
from micro_blog.views import (contact, subscribe, site_blog_home, blog_category, blog_tag, admin_post_list, new_post, edit_blog_post,
                              admin_category_list, new_blog_category, blog_category,
                              blog_article, archive_posts, delete_category, empty,
                              edit_category, change_category_status, thankyou_page)
import microsite_front
from pages.views import site_page, set_country
from microsite_front.xml import rss, blog_rss, sitemap_xml, facebook_rss
from microsite_front.views import index, tools, url_checker_tool, s3_objects_set_metadata, sitemap, books, oss, servicee


from search.views import autocomplete
from django.views.static import serve
from .country_urls import country_patterns
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'_static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR + '/books/templates/html/_static/'}),
    url(r'_sources/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR + '/books/templates/html/_sources/'}),
    url(r'^$', index),
    url(r'^books/(?P<path>.*)$', books),
    url(r'^tools/$', tools, name='tools'),
    url(r'^tools/url-checker/$', url_checker_tool, name='url_checker_tool'),
    url(r'^tools/set-meta-data-for-S3-objects/$', s3_objects_set_metadata, name='s3_objects_set_metadata'),

    url(r'^subscribe/$', subscribe),
    # url(r'^servicee/$', servicee),

    url(r'^set_country/$', set_country, name="set_country"),

    url(r'^forum/', include('django_simple_forum.urls', namespace="django_simple_forum")),

    url(r'^portal/', include('micro_admin.urls', namespace='micro_admin')),
    url(r'^contact-india/$', contact, name="contact_india"),

    url(r'^thank-you/$', thankyou_page, name="thankyou_page"),

    url(r'^contact-usa/$', contact, name="contact_usa"),
    url(r'^contact-aus/$', contact, name="contact_usa"),
    url(r'^contact-uk/$', contact, name="contact_usa"),
    url(r'^contact-uae/$', contact, name="contact_uae"),


    url(r'^blog/list/$', admin_post_list, name='admin_post_list'),
    url(r'^blog/new-post/$', new_post, name='new_post'),
    url(r'^blog/edit-post/(?P<blog_slug>[-\w]+)/$', edit_blog_post, name='edit_blog_post'),
    url(r'^blog/category-list/$', admin_category_list, name='admin_category_list'),
    url(r'^blog/new-category/$', new_blog_category, name='new_blog_category'),

    url(r'^blog/(?P<page_num>[-\0-9]+)/', site_blog_home, name="site_blog_home"),

    url(r'^blog/(?P<slug>[-\w]+)/$', blog_article, name='blog_article'),
    url(r'^blog/(?P<year>\w{0,})/(?P<month>w{0,})/$', archive_posts),

    url(r'^blog/edit-category/(?P<category_slug>[-\w]+)/$', edit_category, name='edit_blog_category'),
    url(r'^blog/delete-category/(?P<category_slug>[-\w]+)/$', delete_category, name='delete_blog_category'),
    url(r'^blog/category/status/(?P<category_slug>[-\w]+)/$', change_category_status, name='change_category_status'),

    url(r'^blog/category/(?P<slug>[-\w]+)/$', blog_category, name="blog_category"),
    url(r'^blog/category/(?P<slug>[-\w]+)/(?P<page_num>[-\w]+)/$', blog_category, name="blog_category"),

    url(r'^blog/$', site_blog_home, name="site_blog_home"),

    url(r'^portal/content/', include('pages.urls', namespace='pages')),
    url(r'^sitemap.xml$', sitemap_xml, name="sitemap_xml"),
    # url(r'^sitemap-(?P<country_name>[-\w]+).xml/$', sitemap_xml, name="sitemap_xml"),

    url(r'^sitemap/$', sitemap),
    url(r'^empty/$', empty),
    url(r'^sitemap-(?P<country_name>[-\w]+)/$', sitemap, name="sitemap"),
    url(r'^sitemap-(?P<country_name>[-\w]+)/(?P<page_num>[-\w]+)/$', sitemap, name="sitemap"),
    url(r'^sitemap/(?P<page_num>[-\w]+)/$', sitemap, name="sitemap"),

    url(r'^(?P<slug>[-\w]+)/$', site_page),
    url(r'^facebook.rss$', facebook_rss),
    url(r'^rss.xml$', rss),
    url(r'^blog.rss$', blog_rss),

    url(r'^search/autocomplete/$', autocomplete),

]

urlpatterns += country_patterns(
    url(_(r'^$'), index),
    url(r'^contact-india/$', contact, name="contact_india"),
    url(r'^contact-usa/$', contact, name="contact_usa"),
    url(r'^contact-aus/$', contact, name="contact_usa"),
    url(r'^contact-uk/$', contact, name="contact_usa"),
    url(r'^contact-uae/$', contact, name="contact_uae"),
    url(r'^sitemap.xml$', sitemap_xml, name="sitemap_xml"),
    url(r'^(?P<slug>[-\w]+)/$', site_page),

)


handler404 = microsite_front.views.handler404
handler500 = microsite_front.views.handler500

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG is False:   # if DEBUG is True it will be served automatically
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
