from django.conf.urls import patterns, url

urlpatterns = patterns('employee',

    url(r'^$', 'views.reports_list', name='reports_list'),
    url(r'^reports/new/$', 'views.new_report', name='new_report'),
    url(r'^leaves/new/$', 'views.new_leave', name='new_leave'),
    url(r'^leaves/$', 'views.leaves_list', name='leaves_list'),
    url(r'^leaves/edit/(?P<pk>[a-zA-Z0-9_-]+)/$','views.edit_leaves',name='edit_leaves'),
    url(r'^leaves/delete/(?P<pk>[a-zA-Z0-9_-]+)/$','views.delete_leaves',name='delete_leaves'),
    url(r'^leaves/view/(?P<pk>[a-zA-Z0-9_-]+)/$', 'views.view_leaves', name='view_leaves'),
    url(r'^reports/(?P<pk>[a-zA-Z0-9_-]+)/$', 'views.employee_report', name='employee_report'),
    url(r'^leaves/(?P<pk>[a-zA-Z0-9_-]+)/$', 'views.employee_leaves', name='employee_leaves'),
    url(r'^reports/view/(?P<pk>[a-zA-Z0-9_-]+)/$', 'views.view_report', name='view_report'),
    url(r'^reports/edit/(?P<pk>[a-zA-Z0-9_-]+)/$','views.edit_report',name='edit_report'),
    url(r'^reports/delete/(?P<pk>[a-zA-Z0-9_-]+)/$','views.delete_report',name='delete_report'),
)
