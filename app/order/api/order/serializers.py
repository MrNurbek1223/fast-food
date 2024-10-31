from rest_framework import serializers
from .models import Order, OrderItem, FoodItem, Branch
from rest_framework_gis.fields import GeometryField
from django.contrib.gis.geos import Point


class OrderSerializerGET(serializers.ModelSerializer):
    branch_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'branch', 'delivery_address', 'total_time', 'total_price', 'branch_id']


class OrderItemSerializer(serializers.ModelSerializer):
    food_item_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['food_item_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    branch_id = serializers.IntegerField()
    location = serializers.DictField()

    class Meta:
        model = Order
        fields = ['branch_id', 'delivery_address', 'location', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        branch = Branch.objects.get(id=validated_data.pop('branch_id'))
        user = self.context['request'].user

        location_data = validated_data.pop('location')
        latitude, longitude = location_data['coordinates']
        location_point = Point(longitude, latitude)

        order = Order.objects.create(
            branch=branch,
            user=user,
            location=location_point,
            **validated_data
        )

        total_price = 0
        order_items = [
            OrderItem(
                order=order,
                food_item=FoodItem.objects.get(id=item['food_item_id']),
                quantity=item['quantity']
            )
            for item in items_data
        ]
        total_price += sum(item.food_item.price * item.quantity for item in order_items)

        OrderItem.objects.bulk_create(order_items)
        order.total_price = total_price
        order.save()

        return order


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'location']


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['total_price', 'total_time', 'status']
