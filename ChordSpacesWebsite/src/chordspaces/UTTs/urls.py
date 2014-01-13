from django.conf.urls import patterns, url

from UTTs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<mode_1>\d+)/(?P<major_interval_1>\d+)/$', views.Graph2D, name='Graph2D'),
    url(r'^(?P<mode_1>[\+-])/(?P<major_interval_1>\d+)/(?P<minor_interval_1>\d+)/(?P<name_1>[a-zA-Z]{1})/(?P<mode_2>[\+-])/(?P<major_interval_2>\d+)/(?P<minor_interval_2>\d+)/(?P<name_2>[a-zA-z]{1})/$', views.Graph2D, name='Graph2D'),
    url(r'^(?P<mode_1>[\+-])/(?P<major_interval_1>\d+)/(?P<minor_interval_1>\d+)/(?P<name_1>[a-zA-Z]{1})/(?P<mode_2>[\+-])/(?P<major_interval_2>\d+)/(?P<minor_interval_2>\d+)/(?P<name_2>[a-zA-z]{1})/(?P<x1>\d+)/(?P<y1>\d+)/(?P<x2>\d+)/(?P<y2>\d+)(?:/(?P<shortcut>[a-zA-z-1.]+))?/$', views.GraphPath, name='GraphPath'),
    url(r'^(?P<mode_1>[\+-])/(?P<major_interval_1>\d+)/(?P<minor_interval_1>\d+)/(?P<name_1>[a-zA-Z]{1})/(?P<mode_2>[\+-])/(?P<major_interval_2>\d+)/(?P<minor_interval_2>\d+)/(?P<name_2>[a-zA-z]{1})/(?P<transString>[a-zA-z-1.]+)/$', views.GraphWithShortcut, name='GraphWithShortcut'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)