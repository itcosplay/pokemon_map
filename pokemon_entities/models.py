from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    next_evolution = models.ForeignKey (
        'self', 
        on_delete=SET_NULL,
        null = True,
        blank=True,
        related_name='+'
    )
    previous_evolution = models.ForeignKey (
        'self', 
        on_delete=SET_NULL,
        null = True,
        blank=True,
        related_name='+'
    )

    def __str__(self):

        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=CASCADE)
    latitude = models.FloatField(null=True, verbose_name='Lat')
    lontitude = models.FloatField(null=True, verbose_name='Lon')
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)

    def __str__(self):

        return f'{self.pokemon.title}'