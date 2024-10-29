from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .filters import OrderFilter
from .models import Order
from .pagination import CustomPageNumberPagination
from .serializers import OrderSerializerGET, OrderSerializer
from rest_framework.views import APIView
from .permissions import BranchAdminPermission
from app.branch.api.branch.models import Branch
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .services import OrderService



class AdminOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializerGET
    permission_classes = [IsAuthenticated, BranchAdminPermission]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        user = self.request.user
        branch_ids = Branch.objects.filter(admin=user).values_list('id', flat=True)
        return Order.objects.filter(branch_id__in=branch_ids)


class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({
            "order_id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "delivery_latitude": order.delivery_latitude,
            "delivery_longitude": order.delivery_longitude,
        }, status=status.HTTP_201_CREATED)


class OrderStatusChangeView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            status_to_set = request.data.get('status')

            if not status_to_set:
                return Response({"detail": "Status ko'rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)

            updated_order = OrderService.change_status(order, status_to_set, request.user)

            return Response({
                "detail": f"Buyurtma holati '{status_to_set}' ga o'zgartirildi.",
                "total_price": updated_order.total_price,
                "total_time": updated_order.total_time
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
