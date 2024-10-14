from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.views import APIView
from .permissions import BranchAdminPermission
from app.branch.api.branch.models import Branch
from app.food.api.food.models import FoodItem
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .services import OrderService
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .utils import calculate_preparation_time


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, BranchAdminPermission]

    def get_queryset(self):
        branch = self.request.user.admin_branches.first()
        if not branch:
            raise ValidationError("Sizga hech qanday filial tayinlanmagan.")
        queryset = Order.objects.filter(branch_id=branch.id)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class CreateOrderView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        branch_id = data.get('branch_id')
        delivery_latitude = float(data.get('delivery_latitude'))
        delivery_longitude = float(data.get('delivery_longitude'))
        items = data.get('items')
        branch = Branch.objects.get(id=branch_id)
        user_location = Point(delivery_longitude, delivery_latitude, srid=4326)
        distance = branch.location.distance(user_location) * 100
        pending_orders = Order.objects.filter(
            branch=branch,
            status__in=['ordered', 'preparing']
        ).order_by('created_at')
        total_old_time = 0
        for pending_order in pending_orders:
            total_old_time += calculate_preparation_time(pending_order.order_items.all())
        new_order_items = [
            OrderItem(food_item=FoodItem.objects.get(id=food_item_id), quantity=quantity)
            for food_item_id, quantity in items.items()
        ]
        total_new_time = calculate_preparation_time(new_order_items)
        total_preparation_time = total_old_time + total_new_time
        delivery_time = distance * 3
        total_time = total_preparation_time + delivery_time
        order = Order.objects.create(
            user=user,
            branch=branch,
            delivery_address=f"{delivery_latitude}, {delivery_longitude}",
            total_price=0
        )

        total_price = 0
        for order_item in new_order_items:
            order_item.order = order
            order_item.save()
            total_price += order_item.food_item.price * order_item.quantity

        order.total_price = total_price
        order.total_time = int(total_time)
        order.save()

        return Response({
            "order_id": order.id,
            "total_price": total_price,
            "total_time": total_time,
            "distance_km": round(distance, 2)
        }, status=status.HTTP_201_CREATED)


class OrderStatusChangeView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            status_to_set = request.data.get('status')

            if not status_to_set:
                return Response({"detail": "Status ko'rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)
            OrderService.change_status(order, status_to_set, request.user)
            return Response({
                "detail": f"Buyurtma holati '{status_to_set}' ga o'zgartirildi."
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
