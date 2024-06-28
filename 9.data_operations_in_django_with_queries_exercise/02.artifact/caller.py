import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# from populate_db import populate_model_with_data
from main_app.models import Pet, Artifact


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(name=name, species=species)

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk = artifact.pk).update(name=new_name)

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()
