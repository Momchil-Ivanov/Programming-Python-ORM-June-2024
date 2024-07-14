import os
from decimal import Decimal

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.core.exceptions import ValidationError
from main_app.models import Customer, Book, Product, DiscountedProduct, SpiderHero, FlashHero

# Create queries within functions
# Create a Product instance
# Create instance of SpiderHero
