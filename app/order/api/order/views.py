from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .filters import OrderFilter
from .models import Order
from .pagination import CustomPageNumberPagination
from .serializers import OrderSerializerGET, OrderSerializer, OrderReadSerializer, OrderStatusSerializer
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

    @swagger_auto_schema(
        operation_summary="Admin uchun filial buyurtmalarini olish",
        responses={200: OrderSerializerGET(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        branch_ids = Branch.objects.filter(admin=user).values_list('id', flat=True)
        return Order.objects.filter(branch_id__in=branch_ids)


class CreateOrderView(APIView):
    @swagger_auto_schema(
        operation_summary="Yangi buyurtma yaratish",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response("Buyurtma muvaffaqiyatli yaratildi", OrderReadSerializer),
            400: "Buyurtmani yaratishda xatolik"
        }
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        read_serializer = OrderReadSerializer(order)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusChangeView(APIView):
    @swagger_auto_schema(
        operation_summary="Buyurtma holatini o'zgartirish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'status': openapi.Schema(type=openapi.TYPE_STRING, description="Yangi holat")}
        ),
        responses={
            200: openapi.Response("Holat muvaffaqiyatli o'zgartirildi", OrderStatusSerializer),
            400: "Status ko'rsatilmagan yoki noto'g'ri",
            404: "Buyurtma topilmadi"
        }
    )
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            status_to_set = request.data.get('status')
            if not status_to_set:
                return Response({"detail": "Status ko'rsatilmagan."}, status=status.HTTP_400_BAD_REQUEST)
            updated_order = OrderService.change_status(order, status_to_set, request.user)
            read_serializer = OrderStatusSerializer(updated_order)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializerGET
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    @swagger_auto_schema(
        operation_summary="Foydalanuvchining buyurtmalarini olish",
        responses={200: OrderSerializerGET(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
