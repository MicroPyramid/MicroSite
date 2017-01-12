from django.conf.urls import url
from micro_blog.views import (site_blog_home, blog_tag, admin_post_list, new_post, edit_blog_post,
                              admin_category_list, new_blog_category, blog_category,
                              blog_article, archive_posts, delete_category,
                              edit_category, change_category_status)

urlpatterns = [
    url(r'^$', site_blog_home, name='site_blog_home'),
    url(r'^tag/(?P<slug>[-\w]+)/$', blog_tag),
    url(r'^list/$', admin_post_list, name='admin_post_list'),
    url(r'^new-post/$', new_post, name='new_post'),
    url(r'^edit-post/(?P<blog_slug>[-\w]+)/$', edit_blog_post, name='edit_blog_post'),
    url(r'^category-list/$', admin_category_list, name='admin_category_list'),
    url(r'^new-category/$', new_blog_category, name='new_blog_category'),
    url(r'^category/(?P<slug>[-\w]+)/$', blog_category, name="blog_category"),
    url(r'^(?P<slug>[-\w]+)/$', blog_article, name='blog_article'),
    url(r'^(?P<year>\w{0,})/(?P<month>\w{0,})/$', archive_posts),
    url(r'^edit-category/(?P<category_slug>[-\w]+)/$', edit_category, name='edit_blog_category'),
    url(r'^delete-category/(?P<category_slug>[-\w]+)/$', delete_category, name='delete_blog_category'),
    url(r'^category/status/(?P<category_slug>[-\w]+)/$', change_category_status, name='change_category_status'),

    # url(r"^ajax/photos/upload/$", upload_photos, name = "upload_photos"),
    # url(r"^ajax/photos/recent/$", recent_photos, name = "recent_photos"),
]
