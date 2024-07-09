import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Mage, Necromancer, UserProfile, Message, Student

# Create queries within functions
# Create instances
# Test cases
student1 = Student(name="Alice", student_id=45.23)
student1.full_clean()
student1.save()
retrieved_student1 = Student.objects.get(name="Alice")

# Print the saved ID of the student1
