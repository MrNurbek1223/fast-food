from django.db import models
from app.branch.api.branch.models import Branch
from app.food.api.food.models import FoodItem
from page.models import User


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ordered', 'Zakaz qilindi'),
        ('preparing', 'Tayyorlanmoqda'),
        ('on_the_way', 'Zakaz yo‘lga chiqdi'),
        ('delivered', 'Yetkazib berildi'),
        ('rejected', 'Zakaz rad etildi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    total_time = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='ordered')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.get_status_display()}"

    def update_status(self, new_status):
        if new_status in dict(self.ORDER_STATUS_CHOICES):
            self.status = new_status
            self.save()
        else:
            raise ValueError("Noto'g'ri status!")



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} (Order {self.order.id})"