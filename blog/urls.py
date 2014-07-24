from django.conf.urls import patterns, include, url


urlpatterns = patterns('blog.views',
    
    url(r'^$', 'home'),
    url(r'^(?P<slug>(\w*\d*)((\w+)-{0,}(\w+)*){0,}((\w+)(\w+)*){0,}).html$','pages.views.page_details'),
)