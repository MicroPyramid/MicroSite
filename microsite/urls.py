from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls')),
    url(r'^portal/', include('microadmin.urls')),
    url(r'^(?P<slug>(\w*\d*)((\w+)-{0,}(\w+)*){0,}((\w+)(\w+)*){0,}).html$','pages.views.page_details'),
)
