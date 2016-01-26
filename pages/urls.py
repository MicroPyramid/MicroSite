from django.conf.urls import url
from pages.views import (pages, new_page, delete_page, edit_page, menu, add_menu, delete_menu,
                         change_menu_status, edit_menu,)

urlpatterns = [

    url(r'^page/$', pages, name='pages'),
    url(r'^page/new/$', new_page, name='new_page'),
    url(r'^page/delete/(?P<pk>\d+)/$', delete_page, name='delete_page'),
    url(r'^page/edit/(?P<pk>\d+)/$', edit_page, name='edit_page'),
    url(r'^menu/$', menu, name='menu'),
    url(r'^menu/new/$', add_menu, name='add_menu'),
    url(r'^menu/delete_menu/(?P<pk>\d+)/$', delete_menu, name='delete_menu'),
    url(r'^menu/status/(?P<pk>\d+)/$', change_menu_status, name='change_menu_status'),
    url(r'^menu/edit/(?P<pk>\d+)/$', edit_menu, name='edit_menu'),

]
