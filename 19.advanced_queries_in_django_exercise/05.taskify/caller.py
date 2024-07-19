import os
from datetime import date

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import VideoGame, Invoice, BillingInfo, Programmer, Project, Technology, Task

# Create BillingInfo instances with real addresses
# Create task instances with custom creation dates
