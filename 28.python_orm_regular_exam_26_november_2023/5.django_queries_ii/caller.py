import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article
from django.db.models import Q, Count, Avg
from django.db import models


# Create queries within functions
def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name and search_email:
        query = Author.objects.filter(
            Q(full_name__icontains=search_name) &
            Q(email__icontains=search_email)
        )
    elif search_name:
        query = Author.objects.filter(full_name__icontains=search_name)
    elif search_email:
        query = Author.objects.filter(email__icontains=search_email)

    # Order by full name in descending order
    query = query.order_by('-full_name')

    result = []

    for a in query:
        banned_status = 'Banned' if a.is_banned else 'Not Banned'
        result.append(f'Author: {a.full_name}, email: {a.email}, status: {banned_status}')

    return '\n'.join(result) if result else ''


def get_top_publisher():
    top_publisher = (Author.objects.annotate(article_count=models.Count('articles')).
                     order_by( '-article_count','email').first())
    if not top_publisher or top_publisher.article_count == 0:
        return ''
    return f'Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles.'


def get_top_reviewer():
    top_reviewer = (Author.objects.annotate(review_count=models.Count('reviews')).
                    order_by('-review_count', 'email').first())
    if not top_reviewer or top_reviewer.review_count == 0:
        return ''
    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews.'


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()
    if not latest_article:
        return ''
    authors = latest_article.authors.order_by('full_name')
    author_names = ', '.join(author.full_name for author in authors)
    review_data = latest_article.reviews.aggregate(
        num_reviews=Count('id'),
        avg_rating=Avg('rating')
    )

    num_reviews = review_data['num_reviews'] or 0
    avg_rating = review_data['avg_rating'] or 0.0
    avg_rating_formatted = f"{avg_rating:.2f}"
    return (f"The latest article is: {latest_article.title}. "
            f"Authors: {author_names}. "
            f"Reviewed: {num_reviews} times. "
            f"Average Rating: {avg_rating_formatted}.")


def get_top_rated_article():
    top_rated_article = (Article.objects.annotate(avg_rating=Avg('reviews__rating')).
                         order_by('-avg_rating','title').first())
    if not top_rated_article or top_rated_article.reviews.count() == 0:
        return ''

    review_data = top_rated_article.reviews.aggregate(
        num_reviews=Count('id'),
        avg_rating=Avg('rating')
    )

    num_reviews = review_data['num_reviews'] or 0
    avg_rating = review_data['avg_rating'] or 0.0
    avg_rating_formatted = f"{avg_rating:.2f}"
    return (f"The top-rated article is: {top_rated_article.title}, with an average "
            f"rating of {avg_rating_formatted}, reviewed {num_reviews} times.")


def ban_author(email=None):
    if email is None:
        return 'No authors banned.'
    author = Author.objects.filter(email=email).first()
    if not author:
        return 'No authors banned.'
    review_data = author.reviews.aggregate(
        num_reviews=Count('id')
    )

    num_reviews = review_data['num_reviews'] or 0
    author.is_banned = True
    author.save()

    author.reviews.all().delete()
    return f'Author: {author.full_name} is banned! {num_reviews} reviews deleted.'
