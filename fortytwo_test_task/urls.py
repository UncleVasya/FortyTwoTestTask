from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('apps.person.urls', namespace='person')),
    url(r'^requests/', include('apps.requestlog.urls', namespace='requestlog')),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout,
        {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
