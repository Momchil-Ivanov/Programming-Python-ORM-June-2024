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


def find_authors_nationalities() -> str:
    authors = Author.objects.exclude(nationality=None)
    return "\n".join([f"{author.first_name} {author.last_name} is {author.nationality}" for author in authors])


def order_books_by_year() -> str:
    ordered_books = Book.objects.order_by("publication_year", "title")
    return "\n".join([f"{book.publication_year} year: {book.title} by {book.author}" for book in ordered_books])


def delete_review_by_id(review_id) -> str:
    review = Review.objects.get(id=review_id)
    review.delete()
    return f"Review by {review.reviewer_name} was deleted"


def filter_authors_by_nationalities(nationality) -> str:
    result = []
    authors = Author.objects.filter(nationality=nationality).order_by("first_name", "last_name")
    for a in authors:
        result.append(f"{a.biography}") if a.biography else result.append(f"{a.first_name} {a.last_name}")
    return "\n".join(result)


def filter_authors_by_birth_year(start_year, end_year) -> str:
    authors = Author.objects.filter(birth_date__year__range=(start_year, end_year)).order_by('-birth_date')
    return "\n".join([f"{author.birth_date}: {author.first_name} {author.last_name}" for author in authors])
