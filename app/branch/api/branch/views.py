from django.shortcuts import render
from .serializers import BranchSerializer
from .models import Branch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions, status, generics
from page.permissions import IsAdminOrWaiter
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'admin':
            longitude = self.request.data.get('longitude')
            latitude = self.request.data.get('latitude')
            if longitude and latitude:
                location = Point(float(longitude), float(latitude), srid=4326)
                serializer.save(location=location)
            else:
                raise PermissionDenied("Filial joylashuvini to'liq kiriting.")
        else:
            raise PermissionDenied("Faqat adminlar filial yaratishi mumkin.")

    def perform_update(self, serializer):
        branch = self.get_object()
        if self.request.user.role == 'admin' or self.request.user == branch.admin:
            longitude = self.request.data.get('longitude')
            latitude = self.request.data.get('latitude')
            if longitude and latitude:
                location = Point(float(longitude), float(latitude), srid=4326)
                serializer.save(location=location)
            else:
                serializer.save()
        else:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialni o'zgartira olasiz.")

    def perform_destroy(self, instance):
        if self.request.user.role == 'admin' or self.request.user == instance.admin:
            instance.delete()
        else:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialni o'chira olasiz.")


class NearestBranchView(APIView):
    def get(self, request):
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))

        user_location = Point(longitude, latitude, srid=4326)
        branches = Branch.objects.annotate(distance=Distance('location', user_location)).order_by('distance')[:5]

        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)
