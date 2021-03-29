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
    club_years = position = models.CharField(max_length=40, null=True, blank=True)
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

    def calculate_importance(self):
        years_for_club_list = self.club_years.replace(",", " ").replace("-", " ")
        years_for_club_list = [int(s) for s in years_for_club_list.split() if s.isdigit()]
        years_for_club = 0
        if (len(years_for_club_list) % 2) != 0:
            years_for_club = int(datetime.datetime.now().year) - years_for_club_list[-1]
            years_for_club_list.pop()
        for y in range(len(years_for_club_list), 1, -2):
            years_for_club += years_for_club_list[y-1] - years_for_club_list[y-2]
        contribution = (self.games / years_for_club) * (1/50)
        club_age = int(datetime.datetime.now().year) - self.team.founded_in
        club_titles = self.team.national_honors + self.team.international_honors
        importance = ((contribution * self.honors) / years_for_club) * (club_age / club_titles)
        #importance = "{:.2f}".format(((contribution * self.honors) / years_for_club) * (club_age / club_titles))
        return importance

    def calculate_importance_normalized(self):
        club_players = Player.objects.filter(team=self.team)
        importance_list = []
        for p in club_players:
            importance_list.append(p.calculate_importance())
        max_club_importance = max(importance_list)
        normalized_importance = "{:.2f}".format(self.calculate_importance() * (10/max_club_importance))
        return normalized_importance



    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.person.name

    def get_absolute_url(self):
        return reverse('allstar_player_detail', args=[self.id, self.slug])