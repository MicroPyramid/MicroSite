from django.conf.urls import url
from employee.views import reports_list, new_report, employee_report, view_report, edit_report, delete_report

urlpatterns = [
    url(r'^$', reports_list, name='reports_list'),
    url(r'^reports/new/$', new_report, name='new_report'),
    url(r'^reports/(?P<pk>[a-zA-Z0-9_-]+)/$', employee_report, name='employee_report'),
    url(r'^reports/view/(?P<pk>[a-zA-Z0-9_-]+)/$', view_report, name='view_report'),
    url(r'^reports/edit/(?P<pk>[a-zA-Z0-9_-]+)/$', edit_report, name='edit_report'),
    url(r'^reports/delete/(?P<pk>[a-zA-Z0-9_-]+)/$', delete_report, name='delete_report'),
]
