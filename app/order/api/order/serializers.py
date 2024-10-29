from rest_framework import serializers
from .models import Order, OrderItem, FoodItem, Branch
from rest_framework.exceptions import ValidationError


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'branch', 'delivery_address', 'total_time', 'total_price']


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
    delivery_latitude = serializers.FloatField()
    delivery_longitude = serializers.FloatField()

    class Meta:
        model = Order
        fields = ['branch_id', 'delivery_address', 'delivery_latitude', 'delivery_longitude', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        branch = Branch.objects.get(id=validated_data.pop('branch_id'))
        user = self.context['request'].user
        order = Order.objects.create(
            branch=branch,
            user=user,
            delivery_latitude=validated_data.pop('delivery_latitude'),
            delivery_longitude=validated_data.pop('delivery_longitude'),
            **validated_data
        )
        total_price = sum(
            FoodItem.objects.get(id=item['food_item_id']).price * item['quantity']
            for item in items_data
        )
        order_items = [
            OrderItem(
                order=order,
                food_item=FoodItem.objects.get(id=item['food_item_id']),
                quantity=item['quantity']
            )
            for item in items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        order.total_price = total_price
        order.save()

        return order