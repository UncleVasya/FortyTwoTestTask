from django.conf.urls import patterns, url
from django.views.decorators.http import require_http_methods

from apps.requestlog import views

urlpatterns = patterns(
    '',
    url(r'^$', views.RequestsView.as_view(), name='requests'),

    url(r'^(?P<pk>\d+)/update$',
        require_http_methods(['POST'])(views.RequestUpdateView.as_view()),
        name='request_update'),
)
