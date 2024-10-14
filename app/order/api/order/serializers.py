from rest_framework import serializers
from .models import Order
from django.contrib.auth import authenticate

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'branch', 'delivery_address', 'total_time', 'total_price']