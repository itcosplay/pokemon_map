import folium

from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Pokemon
from .models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]

DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon (
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker (
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon (
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.lontitude,
            pokemon_entity.pokemon.image.path
        )

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append ({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render (
        request, 
        'mainpage.html', 
        context = {
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_on_page,
        }
    )


def show_pokemon(request, pokemon_id):
    try:
        pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    
    except Http404:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    pokemon_entities = pokemon.entities.all()
    
    pokemon_data = {
        'pokemon_id': pokemon_id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(pokemon.image.url)
    }

    if pokemon.next_evolution is not None:
        next_evolution_data = {
            'title': pokemon.next_evolution.title,
            'pokemon_id': pokemon.next_evolution.id,
            'img_url': request.build_absolute_uri (
                pokemon.next_evolution.image.url
            )
        }
        pokemon_data['next_evolution'] = next_evolution_data

    if pokemon.previous_evolution is not None:
        previous_evolution_data = {
            'title': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri (
                pokemon.previous_evolution.image.url
            )
        }
        pokemon_data['previous_evolution'] = previous_evolution_data

    pokemon_entities_on_map = []

    for pokemon_entity in pokemon_entities:
        pokemon_entity_data = {
            'level': pokemon_entity.level,
            'lat': pokemon_entity.latitude,
            'lon': pokemon_entity.lontitude
        }
        
        pokemon_entities_on_map.append(pokemon_entity_data)

    pokemon_data['entities'] = pokemon_entities_on_map

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_data['entities']:
        add_pokemon (
            folium_map,
            pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon_data['img_url']
        )

    return render (
        request,
        'pokemon.html',
        context = {
            'map': folium_map._repr_html_(),
            'pokemon': pokemon_data
        }
    )
