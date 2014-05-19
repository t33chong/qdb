from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'hunger', include('hunger.urls')),
    url(r'', include('app.urls', namespace='app')),
    )
