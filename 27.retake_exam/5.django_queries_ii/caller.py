import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Min, F, Avg, Max
from main_app.models import House, Dragon, Quest
from decimal import Decimal
from datetime import datetime
# Create queries within functions


def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    houses = House.objects.filter(
        Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)
    ).order_by('-wins', 'name')

    if not houses.exists():
        return "No houses match your search."

    results = []
    for house in houses:
        motto = house.motto if house.motto else "N/A"
        results.append(f"House: {house.name}, wins: {house.wins}, motto: {motto}")

    return "\n".join(results)


def get_most_dangerous_house():
    houses = House.objects.annotate(num_of_dragons=Count('dragons')).order_by('-num_of_dragons', 'name')

    if not houses.exists():
        return "No relevant data."

    most_dangerous_house = houses.first()

    if most_dangerous_house is None or most_dangerous_house.num_of_dragons == 0:
        return "No relevant data."

    ruling_status = "ruling" if most_dangerous_house.is_ruling else "not ruling"

    result = f"The most dangerous house is the House of {most_dangerous_house.name} with {most_dangerous_house.num_of_dragons} dragons. Currently {ruling_status} the kingdom."

    return result


def get_most_powerful_dragon():
    dragons = Dragon.objects.filter(is_healthy=True).annotate(num_quests=Count('quests')).order_by('-power', 'name')

    if not dragons.exists():
        return "No relevant data."

    most_powerful_dragon = dragons.first()

    if most_powerful_dragon is None:
        return "No relevant data."

    power_level = f"{most_powerful_dragon.power:.1f}"

    result = (f"The most powerful healthy dragon is {most_powerful_dragon.name} with a power level of {power_level}, "
              f"breath type {most_powerful_dragon.breath}, and {most_powerful_dragon.wins} wins, coming from the house of "
              f"{most_powerful_dragon.house.name}. Currently participating in {most_powerful_dragon.num_quests} quests.")

    return result


def update_dragons_data():
    decrement_value = Decimal('0.1')

    injured_dragons = Dragon.objects.filter(is_healthy=False)

    num_of_dragons_affected = 0

    for dragon in injured_dragons:
        new_power = dragon.power - decrement_value

        if new_power >= Decimal('1.0'):
            dragon.power = new_power
            dragon.is_healthy = True
            dragon.save()
            num_of_dragons_affected += 1

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    min_power_formatted = f"{min_power:.1f}"

    result = (
        f"The data for {num_of_dragons_affected} dragon/s has been changed. The minimum power level among all dragons is {min_power_formatted}")

    return result


def get_earliest_quest():
    earliest_quest = Quest.objects.order_by('start_time').first()

    if not earliest_quest:
        return "No relevant data."

    quest_name = earliest_quest.name
    quest_code = earliest_quest.code
    start_time = earliest_quest.start_time
    host_name = earliest_quest.host.name

    day = start_time.day
    month = start_time.month
    year = start_time.year

    dragons = earliest_quest.dragons.order_by('-power', 'name')
    dragon_names = [dragon.name for dragon in dragons]

    avg_power_level = dragons.aggregate(Avg('power'))['power__avg']

    if avg_power_level is None:
        avg_power_level = 0.0

    avg_power_level_formatted = f"{avg_power_level:.2f}"

    dragon_names_str = '*'.join(dragon_names)

    result = (
        f"The earliest quest is: {quest_name}, code: {quest_code}, "
        f"start date: {day}.{month}.{year}, host: {host_name}. "
        f"Dragons: {dragon_names_str}. Average dragons power level: {avg_power_level_formatted}"
    )

    return result


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code=quest_code).first()

    if not quest:
        return "No such quest."

    dragons = quest.dragons.all()

    winning_dragon = dragons.order_by('-power', 'name').first()

    winning_dragon.wins += 1
    winning_dragon.save()

    house = winning_dragon.house
    house.wins += 1
    house.save()

    quest_reward = quest.reward

    quest_name = quest.name
    dragon_name = winning_dragon.name
    house_name = house.name
    dragon_wins = winning_dragon.wins
    house_wins = house.wins
    quest_reward_formatted = f"{quest_reward:.2f}"

    quest.delete()

    result = (
        f"The quest: {quest_name} has been won by dragon {dragon_name} "
        f"from house {house_name}. The number of wins has been updated as follows: "
        f"{dragon_wins} total wins for the dragon and {house_wins} total wins for the house. "
        f"The house was awarded with {quest_reward_formatted} coins."
    )

    return result
