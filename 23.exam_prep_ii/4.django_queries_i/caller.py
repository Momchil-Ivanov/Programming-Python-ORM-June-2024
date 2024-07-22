import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order
from django.db.models import Q


# Create and run your queries within functions
def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query = Profile.objects.filter(Q(full_name__icontains=search_string)
                                   | Q(email__icontains=search_string)
                                   | Q(phone_number__icontains=search_string)).order_by('full_name')

    if query is None:
        return ''

    result = []

    for p in query:
        num_of_orders = p.orders.count()
        result.append(f'Profile: {p.full_name}, email:'
                      f' {p.email}, phone number: {p.phone_number}, orders: {num_of_orders}')

    return '\n'.join(result)


def get_loyal_profiles():
    query = Profile.objects.get_regular_customers()

    if query is None:
        return ''

    result = []

    for p in query:
        result.append(f'Profile: {p.full_name}, orders: {p.orders_count}')

    return '\n'.join(result)


def get_last_sold_products():
    try:
        latest_order = Order.objects.prefetch_related('products').latest('creation_date')
        latest_products = latest_order.products.all().order_by('name')
        if latest_products:
            last_sold_products_str = ", ".join(product.name for product in latest_products)
            return f"Last sold products: {last_sold_products_str}"
        return ''
    except Order.DoesNotExist:
        return ''
