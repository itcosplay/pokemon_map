from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    title_en = models.CharField (
        max_length=200, 
        blank=True,
        verbose_name='Имя покемона (Eng.)'
    )
    title_jp = models.CharField (
        max_length=200,
        blank=True,
        verbose_name='Имя покемона (Jap.)'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, verbose_name='Изображение')
    next_evolution = models.ForeignKey (
        'self', 
        on_delete=SET_NULL,
        null = True,
        blank=True,
        related_name='+',
        verbose_name='Эволюционирует в'
    )
    previous_evolution = models.ForeignKey (
        'self', 
        on_delete=SET_NULL,
        null = True,
        blank=True,
        verbose_name='Эволюционировал из'
    )

    def __str__(self):

        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey (
        Pokemon,
        on_delete=CASCADE,
        related_name='entities',
        verbose_name='Вид покемона'
    )
    latitude = models.FloatField(null=True, verbose_name='Lat')
    lontitude = models.FloatField(null=True, verbose_name='Lon')
    appeared_at = models.DateTimeField(null=True, verbose_name='Появление')
    disappeared_at = models.DateTimeField (
        null=True,
        verbose_name='Исчезнет'
    )
    level = models.IntegerField (
        null=True,
        blank=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField (
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField (
        null=True,
        blank=True,
        verbose_name='Сила',
    )
    defence = models.IntegerField (
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField (
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )

    def __str__(self):

        return f'{self.pokemon.title}'