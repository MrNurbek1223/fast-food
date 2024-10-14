from django.db import models
from app.branch.api.branch.models import Branch
from app.food.api.food.models import FoodItem
from page.models import User


# Create your models here.
# Buyurtma modeli (oddiy foydalanuvchi buyurtma beradi)
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ordered', 'Zakaz qilindi'),
        ('preparing', 'Tayyorlanmoqda'),
        ('on_the_way', 'Zakaz yo‘lga chiqdi'),
        ('delivered', 'Yetkazib berildi'),
        ('rejected', 'Zakaz rad etildi'),  # Rad etilgan holat qo'shildi
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    total_time = models.IntegerField(default=0)  # Yetkazib berish vaqti
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Umumiy narx
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ordered')  # Buyurtma holati

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.get_status_display()}"

    def set_preparing(self):
        """Buyurtma tayyorlanayotgan holatga o'tadi"""
        self.status = 'preparing'
        self.save()

    def set_on_the_way(self):
        """Buyurtma yo'lga chiqadi"""
        self.status = 'on_the_way'
        self.save()

    def set_delivered(self):
        """Buyurtma yetkazilgan holatga o'tadi"""
        self.status = 'delivered'
        self.save()

    def set_rejected(self):
        """Buyurtma rad etilgan holatga o'tadi"""
        self.status = 'rejected'
        self.save()



