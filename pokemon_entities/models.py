from django.db import models
from django.db.models.deletion import CASCADE


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)

    def __str__(self):

        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=CASCADE)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)