import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

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
    pokemons = Pokemon.objects.all()

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            pokemon_entities = PokemonEntity.objects.filter(id=requested_pokemon.id)

            break

    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    pokemon_json = {
        "pokemon_id": pokemon_id,
        "title_ru": pokemon.title,
        "title_en": pokemon.title_en,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description,
        "img_url": request.build_absolute_uri(pokemon.image.url)
    }

    if not pokemon.next_evolution is None:
        next_evolution_data = {}
        next_evolution_data["title_ru"] = pokemon.next_evolution.title
        next_evolution_data["pokemon_id"] = pokemon.next_evolution
        next_evolution_data["img_url"] = request.build_absolute_uri (
            pokemon.next_evolution.image.url
        )
        pokemon_json["next_evolution"] = next_evolution_data

    if not pokemon.previous_evolution is None:
        next_evolution_data = {}
        next_evolution_data["title_ru"] = pokemon.previous_evolution.title
        next_evolution_data["pokemon_id"] = pokemon.previous_evolution
        next_evolution_data["img_url"] = request.build_absolute_uri (
            pokemon.previous_evolution.image.url
        )
        pokemon_json["previous_evolution"] = next_evolution_data

    pokemon_entities_list = []

    for pokemon_entity in pokemon_entities:
        pokemon_entity_data = {}
        pokemon_entity_data["level"] = pokemon_entity.level
        pokemon_entity_data["lat"] = pokemon_entity.latitude
        pokemon_entity_data["lon"] = pokemon_entity.lontitude
        pokemon_entities_list.append(pokemon_entity_data)

    pokemon_json["entities"] = pokemon_entities_list

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_json["entities"]:
        add_pokemon (
            folium_map,
            pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon_json['img_url']
        )

    return render (
        request,
        'pokemon.html',
        context = {
            'map': folium_map._repr_html_(),
            'pokemon': pokemon_json
        }
    )
