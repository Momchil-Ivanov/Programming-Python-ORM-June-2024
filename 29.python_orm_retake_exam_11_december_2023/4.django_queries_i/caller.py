import os
import django
from django.db.models import Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer
from django.db import models


# Create queries within functions
def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_country is not None:
        query &= Q(country__icontains=search_country)

    tennis_players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not tennis_players.exists():
        return ''

    result = [
        f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}'
        for p in tennis_players
    ]

    return '\n'.join(result)


def get_top_tennis_player():
    top_tennis_player = (TennisPlayer.objects.annotate(wins_count=models.Count('wins'))
                         .order_by('-wins_count', 'full_name').first())
    if not top_tennis_player:
        return ''

    return f'Top Tennis Player: {top_tennis_player.full_name} with {top_tennis_player.wins_count} wins.'


def get_tennis_player_by_matches_count():
    tennis_player_with_most_matches = (TennisPlayer.objects.annotate(matches_count=models.Count('matches'))
                                       .order_by('-matches_count', 'ranking').first())
    if not tennis_player_with_most_matches or tennis_player_with_most_matches.matches_count == 0:
        return ''

    return (f'Tennis Player: {tennis_player_with_most_matches.full_name}'
            f' with {tennis_player_with_most_matches.matches_count} matches played.')
