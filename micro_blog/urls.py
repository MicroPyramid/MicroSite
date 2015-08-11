from django.conf.urls import patterns, url


urlpatterns = patterns('micro_blog.views',
    #frontend urls
    url(r'^$', 'site_blog_home', name='site_blog_home'),
    url(r'^tag/(?P<slug>[-\w]+)/$','blog_tag'),

    #backend urls
    url(r'^list/$', 'admin_post_list', name='admin_post_list'),
    url(r'^new-post/$', 'new_post', name='new_post'),
    url(r'^edit-post/(?P<blog_slug>[-\w]+)/$', 'edit_blog_post', name='edit_blog_post'),
    url(r'^view-post/(?P<blog_slug>[-\w]+)/$', 'view_post', name='view_post'),
    url(r'^category-list/$', 'admin_category_list', name='admin_category_list'),
    url(r'^new-category/$', 'new_blog_category', name='new_blog_category'),
    url(r'^category/(?P<slug>[-\w]+)/$','blog_category'),
    url(r'^(?P<slug>[-\w]+)/$','blog_article', name='blog_article'),
    url(r'^(?P<year>\w{0,})/(?P<month>\w{0,})/$','archive_posts'),
    url(r'^delete-post/(?P<blog_slug>[-\w]+)/$', 'delete_post', name='delete_post'),
    url(r'^edit-category/(?P<category_slug>[-\w]+)/$', 'edit_category', name='edit_blog_category'),
    url(r'^delete-category/(?P<category_slug>[-\w]+)/$', 'delete_category', name='delete_blog_category'),
    # url(r"^ajax/photos/upload/$", "upload_photos",name = "upload_photos"),
    # url(r"^ajax/photos/recent/$", "recent_photos",name = "recent_photos"),

)

