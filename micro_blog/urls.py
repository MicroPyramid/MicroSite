from django.conf.urls import patterns, include, url


urlpatterns = patterns('micro_blog.views',

    url(r'^$', 'index', name='blog_index'),
    url(r'^category/(?P<slug>[-\w]+)/$','blog_category'),
    url(r'^tag/(?P<slug>[-\w]+)/$','blog_tag'),
    url(r'^(?P<slug>[-\w]+)/$','blog_article'),
    url(r'^new/$', 'new', name='new_post'),
)