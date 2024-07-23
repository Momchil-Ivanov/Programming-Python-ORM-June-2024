import os
import django
from django.db.models import Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
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


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = Tournament.objects.filter(surface_type__icontains=surface).order_by('-start_date')

    if not tournaments:
        return ''

    result = []

    for t in tournaments:
        matches_count = t.matches.count()
        result.append(f'Tournament: {t.name}, start date: {t.start_date}, matches: {matches_count}')

    return '\n'.join(result) if result else ''


def get_latest_match_info():
    latest_match = Match.objects.order_by('-date_played', '-id').first()

    if not latest_match:
        return ''

    players = latest_match.players.order_by('full_name')

    if players.count() < 2:
        return ''

    player1_full_name = players[0].full_name
    player2_full_name = players[1].full_name

    winner_full_name = latest_match.winner.full_name if latest_match.winner else 'TBA'
    return (f'Latest match played on: {latest_match.date_played}, '
            f'tournament: {latest_match.tournament.name}, '
            f'score: {latest_match.score}, '
            f'players: {player1_full_name} vs {player2_full_name}, '
            f'winner: {winner_full_name}, '
            f'summary: {latest_match.summary}')


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return 'No matches found.'

    matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')

    if not matches.exists():
        return 'No matches found.'

    result = []

    for m in matches:
        winner_full_name = m.winner.full_name if m.winner else 'TBA'
        result.append(f'Match played on: {m.date_played}, score: {m.score}, winner: {winner_full_name}')

    return '\n'.join(result)
