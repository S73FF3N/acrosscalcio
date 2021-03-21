import datetime

from django.db import models
from django.urls import reverse

POSITION = (
    ("1", "Goalkeeper"),
    ("2", "Defense"),
    ("3", "Midfield"),
    ("4", "Forward"),
)

class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    flag_image = models.ImageField(blank=True, upload_to='flags')

    def __str__(self):
        return self.name

class Illustrator(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    country = models.ForeignKey(Country, default=1, on_delete=models.CASCADE, blank=True)
    twitter = models.URLField(max_length=150, blank=True)
    instagram = models.URLField(max_length=150, blank=True)
    mail = models.EmailField(max_length=100, blank=True)
    webpage = models.URLField(max_length=150, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class AllstarTeam(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    illustrated_by = models.ForeignKey(Illustrator, default=1, on_delete=models.CASCADE,)
    logo_by = models.ForeignKey(Illustrator, default=1, on_delete=models.CASCADE, blank=True, null=True, related_name="logo_illustrator_set")
    slug = models.SlugField(max_length=200, db_index=True)
    country = models.ForeignKey(Country, default=1, on_delete=models.CASCADE,)
    founded_in = models.IntegerField(default=1900)
    logo = models.ImageField(blank=True, upload_to='logos')
    national_honors = models.IntegerField(default=0)
    international_honors = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def players(self):
        return self.player_set.filter(available=True, is_manager=False).exclude(illustration='')

    def manager(self):
        return self.player_set.filter(available=True, is_manager=True).exclude(illustration='')

    def honorable_mentions(self):
        return self.player_set.filter(available=True, illustration='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('allstar_team_detail', args=[self.id, self.slug])

def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.team.name, filename)

def get_upload_path_thumbnail(instance, filename):
    return '{0}/thumbnail/{1}'.format(instance.team.name, filename)

class Person(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    birth_date = models.DateField(default=datetime.date(1969, 10, 19))
    death_date = models.DateField(blank=True, null=True)
    nationality = models.ForeignKey(Country, default=1, on_delete=models.CASCADE, )

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Player(models.Model):
    person = models.ForeignKey(Person, default=1, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100, db_index=True) # to be replaced by person
    birth_date = models.DateField(default=datetime.date(1970, 10, 19)) # to be replaced by person
    death_date = models.DateField(blank=True, null=True) # to be replaced by person
    club_years = position = models.CharField(max_length=40, null=True, blank=True)
    nationality = models.ForeignKey(Country, default=1, on_delete=models.CASCADE,) # to be replaced by person
    slug = models.SlugField(max_length=200, db_index=True)
    team = models.ForeignKey(AllstarTeam, default=1, on_delete=models.CASCADE,)
    is_manager = models.BooleanField(default=False)
    one_club_man = models.BooleanField(default=False)
    position = models.CharField(max_length=20, choices=POSITION, default="4")
    illustration = models.ImageField(blank=True, upload_to=get_upload_path)
    thumbnail = models.ImageField(blank=True, upload_to=get_upload_path_thumbnail)
    still_active = models.BooleanField(default=False)
    games = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    honors = models.IntegerField(default=0)

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def same_person(self):
        same_person = Player.objects.filter(person=self.person)
        same_person = same_person.exclude(illustration="")
        same_person = same_person.exclude(id=self.id)
        return same_person

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('allstar_player_detail', args=[self.id, self.slug])