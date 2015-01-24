from django.conf.urls import patterns, url

urlpatterns = patterns('employee',

    url(r'^$', 'views.reports_list', name='reports_list'),
    url(r'^reports/new/$', 'views.new_report', name='new_report'),
    url(r'^reports/(?P<email>[a-zA-Z0-9_-]+)/$', 'views.employee_report', name='employee_report'),
    url(r'^reports/edit/(?P<pk>[a-zA-Z0-9_-]+)/$','views.edit_report',name='edit_report'),
    url(r'^reports/delete/(?P<pk>[a-zA-Z0-9_-]+)/$','views.delete_report',name='delete_report'),
)
