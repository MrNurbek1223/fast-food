from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser ,IsAuthenticatedOrReadOnly
from .models import  FoodItem
from .serializers import FoodItemSerializer
from rest_framework.views import APIView

class FoodItemViewSetGet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        branch_id = self.request.query_params.get('branch_id')

        if branch_id:
            return FoodItem.objects.filter(branch__id=branch_id)

        return super().get_queryset()


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        branch = serializer.validated_data['branch']
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialga mahsulot qo'sha olasiz.")
        serializer.save()

    def perform_update(self, serializer):
        branch = serializer.instance.branch
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialning mahsulotini o'zgartira olasiz.")
        serializer.save()

    def perform_destroy(self, instance):
        branch = instance.branch
        if self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialning mahsulotini o'chira olasiz.")
        instance.delete()
