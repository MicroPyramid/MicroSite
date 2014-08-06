from django.conf.urls import patterns, include, url

urlpatterns = patterns('payroll',

    url(r'^$', 'views.staff', name='staff'),
)
