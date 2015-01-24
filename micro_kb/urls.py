from django.conf.urls import patterns, url

urlpatterns = patterns('micro_kb',
    url(r'^$', 'views.knowledgebase', name='knowledgebase'),
)
