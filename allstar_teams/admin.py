from django.contrib import admin
from django.shortcuts import redirect
from django import forms

from .models import Country, AllstarTeam, Player, Illustrator, Person

from PIL import Image
import logging
logger = logging.getLogger(__name__)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    def clean_illustration(self):
        illustration_file_field = self.cleaned_data.get('illustration')
        if illustration_file_field:
            try:
                illustration_file = illustration_file_field.file
                with Image.open(illustration_file.name) as image:
                    image.thumbnail((353, 500), Image.ANTIALIAS)
                    image.save(illustration_file, format=image.format)
                    illustration_file_field.file = illustration_file
                    return illustration_file_field
            except IOError:
                logger.exception("Error during image resize.")

    def clean_thumbnail(self):
        thumbnail_file_field = self.cleaned_data.get('thumbnail')
        if thumbnail_file_field:
            try:
                thumbnail_file = thumbnail_file_field.file
                with Image.open(thumbnail_file.name) as image:
                    image.thumbnail((353, 500), Image.ANTIALIAS)
                    image.save(thumbnail_file, format=image.format)
                    thumbnail_file_field.file = thumbnail_file
                    return thumbnail_file_field
            except IOError:
                logger.exception("Error during image resize.")

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Country, CountryAdmin)

class AllstarTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'available']
    list_editable = ['available']
admin.site.register(AllstarTeam, AllstarTeamAdmin)

class PlayerAdmin(admin.ModelAdmin):
    """actions = ['create_persons']

    def create_persons(self, request, queryset):
        player = Player.objects.all()
        for p in player:
            person = Person(name=p.name, birth_date=p.birth_date, death_date=p.death_date, nationality=p.nationality)
            person.save()
            p.person = person
            p.save()
        return redirect("/admin")"""

    list_display = ['person', 'team', 'created', 'updated', 'available']
    list_editable = ['available']
    form = PlayerForm
admin.site.register(Player, PlayerAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'available']
    list_editable = ['available']
admin.site.register(Person, PersonAdmin)

class IllustratorAdmin(admin.ModelAdmin):
    actions = ['send_mail_to_all_illustrators']

    def send_mail_to_all_illustrators(self, request, queryset):
        return redirect('/send_mail_to_all_illustrators/')

    list_display = ['name', 'created', 'updated', 'available']
    list_editable = ['available']
admin.site.register(Illustrator, IllustratorAdmin)
