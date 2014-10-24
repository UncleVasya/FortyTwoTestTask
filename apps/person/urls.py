from django.conf.urls import patterns, url

from apps.person import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^update/$', views.PersonUpdateView.as_view(), name='person_update'),
)
