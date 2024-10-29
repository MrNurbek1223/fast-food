from django.db.models import Sum, F
from .models import  OrderItem


def calculate_delivery_time(distance_km):
    return distance_km * 3


def calculate_total_preparation_time(branch, new_order_items):
    pending_orders = OrderItem.objects.filter(
        order__branch=branch,
        order__status='preparing'
    )

    total_preparation_time = 0

    for item in pending_orders:
        total_preparation_time += ((item.quantity + 3) // 4) * 5
    for item in new_order_items:
        total_preparation_time += ((item.quantity + 3) // 4) * 5

    return total_preparation_time
