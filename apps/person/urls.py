from django.conf.urls import patterns, url

from apps.person import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),  name='index'),
)
