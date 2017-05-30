from django.conf.urls import url

from . import views

app_name = 'cal'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'previous/(?P<page>[0-9]+)/$', views.previous, name='previous'),
    url(r'next/(?P<page>[0-9]+)/$', views.next, name='next'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^form/$', views.form, name='form'),
    url(r'^users/(?P<user_page>[0-9]+)/$', views.users, name='users'),
    url(r'^next_users/(?P<page>[0-9]+)/(?P<user_page>[0-9]+)/$', views.next_users, name='next_users'),
    url(r'^prev_users/(?P<page>[0-9]+)/(?P<user_page>[0-9]+)/$', views.prev_users, name='prev_users'),
    url(r'^testindex/$', views.calendar, name='calendar'),
]
