from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from apps.person import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^update/$', login_required(views.PersonUpdateView.as_view()),
        name='person_update'),
)
