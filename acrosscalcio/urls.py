from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from allstar_teams.models import AllstarTeam, Player

from .sitemaps import StaticViewSitemap

club_dict = {
    'queryset': AllstarTeam.objects.all(),
    'date_field': 'updated',
}
player_dict = {
    'queryset': Player.objects.all(),
    'date_field': 'updated',
}

sitemaps = {
    'static': StaticViewSitemap,
    'clubs': GenericSitemap(club_dict, priority=0.6),
    'players': GenericSitemap(player_dict, priority=0.4),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('allstar_teams.urls')),
    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
