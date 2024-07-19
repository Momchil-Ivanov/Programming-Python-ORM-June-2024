import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import VideoGame, Invoice, BillingInfo, Programmer, Project, Technology

# Create BillingInfo instances with real addresses
