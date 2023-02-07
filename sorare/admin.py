from django.contrib import admin
from .models import ScoutingResult, FloorPrice

class ScoutingResultAdmin(admin.ModelAdmin):
    list_display = ['lastName', 'playerSlug', 'league', 'position']
admin.site.register(ScoutingResult, ScoutingResultAdmin)


class FloorPriceAdmin(admin.ModelAdmin):
    list_display = ['scouting_result', 'created', 'floorPriceEUR']
admin.site.register(FloorPrice, FloorPriceAdmin)