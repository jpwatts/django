from django.db import models


class Season(models.Model):
    year = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return unicode(self.year)


class Game(models.Model):
    season = models.ForeignKey(Season, related_name='games')
    home = models.CharField(max_length=100)
    away = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s at %s" % (self.away, self.home)


__test__ = {'API_TESTS':"""
Regression test for #11670

>>> season = Season.objects.create(year=2010)
>>> season
<Season: 2010>

>>> Game.objects.create(season=season, home="Houston Astros", away="Chicago Cubs")
<Game: Chicago Cubs at Houston Astros>

>>> Game.objects.all()
[<Game: Chicago Cubs at Houston Astros>]

>>> Game.objects.filter(season__year=2010)
[<Game: Chicago Cubs at Houston Astros>]

>>> Game.objects.get(season__year=2010)
<Game: Chicago Cubs at Houston Astros>

"""}
