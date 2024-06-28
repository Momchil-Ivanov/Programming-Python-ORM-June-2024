import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# from populate_db import populate_model_with_data
from main_app.models import Pet


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)

    return f"{pet.name} is a very cute {pet.species}!"
