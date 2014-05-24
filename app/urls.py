from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns(
    '',
    url('^$', views.index, name='index'),
    url('^all/(?P<page_num>\d+)/$', views.index, name='all'),
    url('^quote/(?P<quote_id>\d+)/$', views.detail, name='detail'),
    url('^tag/(?P<tag_text>\w+)/(?:(?P<page_num>\d+)/)?$',
        views.tag, name='tag'),
    url('^user/(?P<username>\w+)/(?:(?P<page_num>\d+)/)?$',
        views.user, name='user'),
    url('^search/(?:(?P<page_num>\d+)/)?$', views.search, name='search'),
    #url('^search/$', views.search, name='search'),
    url('^signup/$', views.signup, name='signup'),
    url('^login/$', views.log_in, name='login'),
    url('^logout/$', views.log_out, name='logout'),
    url('^submit/$', views.submit, name='submit'),
    )
