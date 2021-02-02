from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^add/(?P<product_id>\d+)/(?P<player_id>\d+)/$', views.cart_add_no_form, name='cart_add_no_form'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^team-autocomplete/$', views.AllstarTeamAutocomplete.as_view(), name='allstarteam-autocomplete'),
    url(r'^player-autocomplete/$', views.PlayerAutocomplete.as_view(), name='player-autocomplete'),
]