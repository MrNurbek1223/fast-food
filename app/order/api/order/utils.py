from django.utils import timezone
from .models import OrderItem, Order


def calculate_delivery_time(distance_km):
    return distance_km * 3


def calculate_total_preparation_time(order):
    current_time = timezone.now()
    total_preparation_time = 0
    branch = order.branch

    pending_orders = Order.objects.filter(branch=branch, status='preparing')
    for pending_order in pending_orders:
        initial_prep_time = pending_order.food_preparation_time
        elapsed_time = (current_time - pending_order.created_at).total_seconds() / 60
        remaining_time = max(initial_prep_time - elapsed_time, 0)
        total_preparation_time += remaining_time

    item_counts = {}
    for item in order.order_items.all():
        food_item_id = item.food_item.id
        item_counts[food_item_id] = item_counts.get(food_item_id, 0) + item.quantity

    new_prep_time = sum(((count + 3) // 4) * 1.25 for count in item_counts.values())
    total_preparation_time += new_prep_time

    return total_preparation_time
