import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

# Run and print your queries


def find_books_by_genre_and_language(genre, language) -> QuerySet:
    return Book.objects.filter(genre=genre, language=language)
