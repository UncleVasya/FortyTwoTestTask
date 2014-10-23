from django.conf.urls import patterns, url

from apps.requestlog import views

urlpatterns = patterns(
    '',
    url(r'^', views.RequestsView.as_view(), name='requests'),
)
