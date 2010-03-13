from django.db import models


class Season(models.Model):
    year = models.PositiveSmallIntegerField()
    world_series_winner = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.year)


class Game(models.Model):
    season = models.ForeignKey(Season, related_name='games')
    home = models.CharField(max_length=100)
    away = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s at %s" % (self.away, self.home)


class Player(models.Model):
    name = models.CharField(max_length=100)
    games = models.ManyToManyField(Game, related_name='players')

    def __unicode__(self):
        return self.name


__test__ = {'API_TESTS':"""
Regression test for #11670

>>> season_2009 = Season.objects.create(year=2009, world_series_winner="New York Yankees")
>>> cardinals_at_astros = season_2009.games.create(home="Houston Astros", away="St. Louis Cardinals")

>>> season_2010 = Season.objects.create(year=2010, world_series_winner="Houston Astros")
>>> cubs_at_astros = season_2010.games.create(home="Houston Astros", away="Chicago Cubs")
>>> brewers_at_astros = season_2010.games.create(home="Houston Astros", away="Milwaukee Brewers")

>>> Game.objects.count()
3

>>> Game.objects.filter(season__year=2010).count()
2

>>> Game.objects.get(season__year=2009)
<Game: St. Louis Cardinals at Houston Astros>

>>> hunter_pence = Player.objects.create(name="Hunter Pence")
>>> hunter_pence.games = Game.objects.filter(season__year__in=[2009, 2010])

>>> hunter_pence.games.count()
3

>>> hunter_pence.games.filter(season__year=2009).count()
1

>>> hunter_pence.games.filter(season__year__exact=2010).count()
2

>>> pudge = Player.objects.create(name="Ivan Rodriquez")
>>> pudge.games = Game.objects.filter(season__year=2009)

>>> pedro_feliz = Player.objects.create(name="Pedro Feliz")
>>> pedro_feliz.games = Game.objects.filter(season__year=2010)

>>> Player.objects.count()
3

>>> Player.objects.filter(games__season__year=2009).distinct().count()
2

>>> Player.objects.filter(games__season__year__exact=2010).distinct().count()
2

>>> Player.objects.filter(games__season__world_series_winner__icontains="Yankees").distinct().count()
2

>>> Player.objects.filter(games__season__world_series_winner__iexact="Houston Astros").distinct().count()
2

"""}
