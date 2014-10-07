from django.conf.urls import patterns, include, url

urlpatterns = patterns('micro_kb',
    url(r'^$', 'views.knowledgebase', name='knowledgebase'),
)
