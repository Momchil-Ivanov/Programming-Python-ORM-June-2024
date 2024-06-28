from django.db import models

# Create your models here.


# class CustomManager(models.Manager):
#     def really_complex_query(self):
#         return "Really complex query"
#
#
# class MyModel(models.Model):
#     field1 = models.CharField(max_length=100)

#     custom_manager = CustomManager()


class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)
