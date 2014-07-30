from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blog/', include('blog.urls')),
    url(r'^portal/', include('microauth.urls')),
    url(r'^(?P<slug>(\w*\d*)((\w+)-{0,}(\w+)*){0,}((\w+)(\w+)*){0,}).html$','pages.views.page_details'),
)
