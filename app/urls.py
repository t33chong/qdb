from django.conf.urls import patterns, url

from updown.views import AddRatingFromModel

from app import views

urlpatterns = patterns(
    '',
    url('^$', views.index, name='index'),
    url('^all/(?P<page_num>\d+)/$', views.index, name='all'),
    url('^quote/(?P<object_id>\d+)/vote/(?P<score>[\d\-]+)/$',
        AddRatingFromModel(),
        {'app_label': 'app', 'model': 'Quote', 'field_name': 'rating'},
        name='vote'),
    url('^quote/(?P<quote_id>\d+)/$', views.detail, name='detail'),
    url('^tag/(?P<tag_text>\w+)/(?:(?P<page_num>\d+)/)?$',
        views.tag, name='tag'),
    url('^user/(?P<username>\w+)/(?:(?P<page_num>\d+)/)?$',
        views.user, name='user'),
    url('^signup/$', views.signup, name='signup'),
    url('^login/$', views.log_in, name='login'),
    url('^logout/$', views.log_out, name='logout'),
    url('^submit/$', views.submit, name='submit'),
    )
