from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        profiles_with_more_than_two_orders = self.annotate(orders_count=Count('orders')).filter(
            orders_count__gt=2
        ).order_by('-orders_count')

        return profiles_with_more_than_two_orders
