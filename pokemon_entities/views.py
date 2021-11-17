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
    print('$$$$$$$$$$$$$$$')
    print()
    print(request.build_absolute_uri(pokemon.image.url))
    print()
    print('$$$$$$$$$$$$$$$')
    
    pokemon = {
        "pokemon_id": pokemon_id,
        "title_ru": pokemon.title,
        "title_en": "Bulbasaur",
        "title_jp": "フシギダネ",
        "description": "cтартовый покемон двойного травяного и ядовитого типа из первого поколения и региона Канто. В национальном покедексе под номером 1. На 16 уровне эволюционирует в Ивизавра. Ивизавр на 32 уровне эволюционирует в Венузавра. Наряду с Чармандером и Сквиртлом, Бульбазавр является одним из трёх стартовых покемонов региона Канто.",
        # "img_url": "https://upload.wikimedia.org/wikipedia/ru/c/ca/%D0%91%D1%83%D0%BB%D1%8C%D0%B1%D0%B0%D0%B7%D0%B0%D0%B2%D1%80.png",
        # "img_url": pokemon.image.path,
        "img_url": request.build_absolute_uri(pokemon.image.url),
        # "entities": [
        #     {
        #         "level": 15,
        #         "lat": 55.753244,
        #         "lon": 37.628423
        #     },
        #     {
        #         "level": 24,
        #         "lat": 55.743244,
        #         "lon": 37.635423
        #     }
        # ],
        "next_evolution": {
            "title_ru": "Ивизавр",
            "pokemon_id": 2,
            "img_url": "https://vignette.wikia.nocookie.net/pokemon/images/7/73/002Ivysaur.png/revision/latest/scale-to-width-down/200?cb=20150703180624&path-prefix=ru"
        }
    }

    pokemon_entities_list = []
    for pokemon_entity in pokemon_entities:
        pokemon_entity_data = {}
        pokemon_entity_data["level"] = pokemon_entity.level
        pokemon_entity_data["lat"] = pokemon_entity.latitude
        pokemon_entity_data["lon"] = pokemon_entity.lontitude
        pokemon_entities_list.append(pokemon_entity_data)

    pokemon["entities"] = pokemon_entities_list

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    # for pokemon_entity in pokemon_entities:
    #     add_pokemon (
    #         folium_map,
    #         pokemon_entity.latitude,
    #         pokemon_entity.lontitude,
    #         pokemon.image.path
    #     )
    for pokemon_entity in pokemon["entities"]:
        add_pokemon (
            folium_map,
            pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render (
        request,
        'pokemon.html',
        context = {
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
