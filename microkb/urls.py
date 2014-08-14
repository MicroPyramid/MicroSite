from django.conf.urls import patterns, include, url

urlpatterns = patterns('microkb',
    url(r'^$', 'views.knowledgebase', name='knowledgebase'),
)
