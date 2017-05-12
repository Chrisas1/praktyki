from django.conf.urls import url

from . import views

app_name = 'week'
urlpatterns = [
    url(r'^$', views.week_sum, name="week_sum"),
]