from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, null=False, blank=False)
    supplier = models.CharField(max_length=100, null=False, blank=False)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
