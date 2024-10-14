from django.utils.timezone import now, timedelta



def calculate_preparation_time(order_items):
    unique_items = {}
    for item in order_items:
        if item.food_item.id in unique_items:
            unique_items[item.food_item.id] += item.quantity
        else:
            unique_items[item.food_item.id] = item.quantity

    total_time = 0
    for quantity in unique_items.values():
        total_time += (quantity // 4) * 5
        if quantity % 4 > 0:
            total_time += 5

    return total_time