from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from .filters import FoodItemFilter
from .models import FoodItem
from .serializers import FoodItemSerializer


class FoodItemViewSetGet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [AllowAny]
    filterset_class = FoodItemFilter

    @swagger_auto_schema(
        operation_summary="Get list of food items",
        responses={200: FoodItemSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve food item details",
        responses={200: FoodItemSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new food item (Branch Admin only)",
        responses={
            201: "Food item created successfully",
            403: "Permission denied"
        }
    )
    def perform_create(self, serializer):
        branch = serializer.validated_data['branch']
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialga mahsulot qo'sha olasiz.")
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Update an existing food item (Branch Admin only)",
        responses={
            200: "Food item updated successfully",
            403: "Permission denied"
        }
    )
    def perform_update(self, serializer):
        branch = serializer.instance.branch
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialning mahsulotini o'zgartira olasiz.")
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Delete a food item (Branch Admin only)",
        responses={
            204: "Food item deleted successfully",
            403: "Permission denied"
        }
    )
    def perform_destroy(self, instance):
        branch = instance.branch
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialning mahsulotini o'chira olasiz.")
        instance.delete()
