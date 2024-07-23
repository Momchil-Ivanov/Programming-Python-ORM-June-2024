import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author
from django.db.models import Q
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
