from rest_framework import serializers
from .models import FoodItem



class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'branch', 'name','category', 'description', 'price']