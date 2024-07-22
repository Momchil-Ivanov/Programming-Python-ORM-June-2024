import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F


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


def get_top_products():
    top_products = Product.objects.annotate(num_orders=Count('order')).filter(num_orders__gt=0).order_by('-num_orders')[:5]

    if not top_products:
        return ''

    result = 'Top products:\n'

    for p in top_products:
        result += f'{p.name}, sold {p.num_orders} times\n'

    return result.strip()


def apply_discounts():
    updated_orders = Order.objects.annotate(num_products=Count('products')).filter(
        num_products__gt=2, is_completed=False).update(total_price=F('total_price') * 0.9)

    return f'Discount applied to {updated_orders} orders.'


def complete_order():
    first_order = Order.objects.prefetch_related('products').filter(is_completed=False).order_by('creation_date').first()

    if not first_order:
        return ''

    for product in first_order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()

    first_order.is_completed = True
    first_order.save()

    return 'Order has been completed!'
