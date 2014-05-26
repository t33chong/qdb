from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password_required/$', 'password_required.views.login'),
    url(r'^likes/$', include('likes.urls'),
    url(r'', include('app.urls', namespace='app')),
    )
