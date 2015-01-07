from django.conf.urls import patterns, url

urlpatterns = patterns('projects',

    url(r'^$', 'views.projects', name='projects'),
)
