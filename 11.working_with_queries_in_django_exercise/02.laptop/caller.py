import os
from typing import List

import django
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
from main_app.models import ArtworkGallery, Laptop, OperatingSystemChoices


# Create and check models
# Run and print your queries


def show_highest_rated_art() -> str:

    highest_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop() -> str:
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.update(
        operation_system=Case(
            When(brand__in=['Asus'], then=Value(OperatingSystemChoices.WINDOWS)),
            When(brand__in=['Apple'], then=Value(OperatingSystemChoices.MACOS)),
            When(brand__in=['Dell', 'Acer'], then=Value(OperatingSystemChoices.LINUX)),
            When(brand__in=['Lenovo'], then=Value(OperatingSystemChoices.CHROME_OS)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()
