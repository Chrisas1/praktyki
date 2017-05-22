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
    url(r'^users/(?P<page>-?[0-9]+)/(?P<day>[0-9]+)/$', views.users, name='users'),
]
