from django.conf.urls import url
from django.urls import path, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
#router.register(r'countries', views.CountriesViewSet)

urlpatterns = [
    url(r'^$', views.AllstarTeamView.as_view()),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.allstar_team_detail, name='allstar_team_detail'),
    url(r'^player/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.allstar_player_detail, name='allstar_player_detail'),
    url(r'^send_mail_to_all_illustrators/$', views.send_mail_to_all_illustrators, name='email'),
]