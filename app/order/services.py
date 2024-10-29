from django.core.exceptions import ValidationError
from api.order.models import Order

class OrderService:
    """
    OrderService buyurtmalar bilan bog'liq amallarni markazlashtiradi
    """

    @staticmethod
    def change_status(order, status, user):
        """
        Buyurtma holatini o'zgartirish va tegishli validatsiyalarni o'tkazish
        """
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

    @staticmethod
    def _set_preparing(order):
        if order.status != 'ordered':
            raise ValidationError("Buyurtma hali qabul qilinmagan.")
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
