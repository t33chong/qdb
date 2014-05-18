from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns(
    '',
    url('^$', views.index, name='index'),
    url('^quote/(?P<quote_id>\d+)/$', views.detail, name='detail'),
    url('^tag/(?P<tag_id>\d+)/$', views.tag, name='tag'),
    url('^submit/$', views.QuoteCreate.as_view(), name='quote_create'),
    )
