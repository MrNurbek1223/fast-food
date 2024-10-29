from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from .utils import calculate_total_preparation_time, calculate_delivery_time


class OrderService:

    @staticmethod
    def change_status(order, status, user):
        if not user.admin_branches.filter(id=order.branch.id).exists():
            raise ValidationError("Siz faqat o‘z filialingizdagi buyurtmalarni boshqarishingiz mumkin.")

        if status == 'preparing':
            OrderService._set_preparing(order)
        elif status == 'on_the_way':
            OrderService._set_on_the_way(order)
        elif status == 'delivered':
            OrderService._set_delivered(order)
        elif status == 'rejected':
            OrderService._set_rejected(order)
        else:
            raise ValidationError("Noma'lum buyurtma holati.")

        return order

    @staticmethod
    def _set_preparing(order):
        if order.status != 'ordered':
            raise ValidationError("Buyurtma hali qabul qilinmagan yoki noto‘g‘ri holatda.")

        if order.delivery_latitude is None or order.delivery_longitude is None:
            raise ValidationError("Yetkazib berish koordinatalari mavjud emas.")

        user_location = Point(order.delivery_longitude, order.delivery_latitude, srid=4326)
        distance_km = order.branch.location.distance(user_location) * 100
        delivery_time = calculate_delivery_time(distance_km)

        new_order_items = order.order_items.all()
        total_preparation_time = calculate_total_preparation_time(order.branch, new_order_items)

        order.total_time = total_preparation_time + delivery_time
        order.total_price = sum(item.food_item.price * item.quantity for item in new_order_items)
        order.status = 'preparing'
        order.save()

    @staticmethod
    def _set_on_the_way(order):
        if order.status != 'preparing':
            raise ValidationError("Buyurtma hali tayyor emas.")
        order.status = 'on_the_way'
        order.save()

    @staticmethod
    def _set_delivered(order):
        if order.status != 'on_the_way':
            raise ValidationError("Buyurtma hali yo'lga chiqmagan.")
        order.status = 'delivered'
        order.save()

    @staticmethod
    def _set_rejected(order):
        if order.status != 'ordered':
            raise ValidationError("Buyurtma hali qabul qilinmagan yoki qayta ishlangan.")
        order.status = 'rejected'
        order.save()
