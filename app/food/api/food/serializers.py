from rest_framework import serializers
from .models import FoodItem
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'branch', 'name', 'description', 'price']