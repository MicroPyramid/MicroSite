from django.conf.urls import patterns, include, url

urlpatterns = patterns('projects',

    url(r'^$', 'views.projects', name='projects'),
)
