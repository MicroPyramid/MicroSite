from django.conf.urls import patterns, url


urlpatterns = patterns('micro_blog.views',
    url(r'^$', 'index', name='blog_index_admin'),
    url(r'^$', 'blog_index', name='blog_index'),
    url(r'^category/(?P<slug>[-\w]+)/$','blog_category'),
    url(r'^new/$', 'new', name='new_post'),
    url(r'^tag/(?P<slug>[-\w]+)/$','blog_tag'),
    
    url(r'^(?P<slug>[-\w]+)/$','blog_article'),
    
    url(r'^edit/(?P<blog_slug>[-\w]+)/$', 'edit_blog_post', name='edit_post'),
    url(r'^change/featured-state/(?P<blog_slug>[-\w]+)/$', 'change_featured_state', name='change_featured_state'),
    url(r'^delete/blog-post/(?P<blog_slug>[-\w]+)/$', 'delete_post', name='delete_post'),

    url(r'^category-list/$', 'blog_category_list', name='blog_category_list'),
    url(r'^new-category/$', 'new_category', name='new_blog_category'),
    url(r'^edit-category/(?P<category_slug>[-\w]+)/$', 'edit_category', name='edit_blog_category'),
    url(r'^delete-category/(?P<category_slug>[-\w]+)/$', 'delete_category', name='delete_blog_category'),

    url(r"^ajax/photos/upload/$", "upload_photos",name = "upload_photos"),
    url(r"^ajax/photos/recent/$", "recent_photos",name = "recent_photos"),
)