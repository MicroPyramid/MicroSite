from django.conf.urls import patterns, include, url


urlpatterns = patterns('micro_blog.views',
    
    url(r'^$', 'index', name='blog_index'),
    url(r'^new/$', 'new', name='new_post'),
)