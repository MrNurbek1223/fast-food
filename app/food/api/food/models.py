from django.db import models
from app.branch.api.branch.models import Branch

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='food_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.branch.name}) - {self.category.name if self.category else 'Uncategorized'}"