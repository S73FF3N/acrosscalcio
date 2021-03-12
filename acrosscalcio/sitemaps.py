from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['club_allstar_team_list', 'disclaimer', 'privacy']

    def location(self, item):
        return reverse(item)