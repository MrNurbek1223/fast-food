from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .pagination import NearestBranchPagination
from .serializers import BranchSerializer
from .models import Branch
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new branch (Admin only)",
        responses={
            201: "Branch created successfully",
            403: "Permission denied"
        }
    )
    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Faqat adminlar filial yaratishi mumkin.")
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Update a branch (Admin or Branch Manager)",
        responses={
            200: "Branch updated successfully",
            403: "Permission denied"
        }
    )
    def perform_update(self, serializer):
        branch = self.get_object()
        if self.request.user.role != 'admin' and self.request.user != branch.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialni o'zgartira olasiz.")
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Delete a branch (Admin or Branch Manager)",
        responses={
            204: "Branch deleted successfully",
            403: "Permission denied"
        }
    )
    def perform_destroy(self, instance):

        if self.request.user.role != 'admin' and self.request.user != instance.admin:
            raise PermissionDenied("Siz faqat o'zingiz boshqaradigan filialni o'chira olasiz.")
        instance.delete()


class NearestBranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]
    pagination_class = NearestBranchPagination

    @swagger_auto_schema(
        operation_summary="List nearest branches",
        manual_parameters=[
            openapi.Parameter('latitude', openapi.IN_QUERY, description="User's latitude", type=openapi.TYPE_NUMBER),
            openapi.Parameter('longitude', openapi.IN_QUERY, description="User's longitude", type=openapi.TYPE_NUMBER),
        ],
        responses={200: BranchSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude and longitude:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            branches = Branch.objects.annotate(distance=Distance('location', user_location)).order_by('distance')
        else:
            branches = Branch.objects.all()

        page = self.paginate_queryset(branches)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(branches, many=True)
        return Response(serializer.data)
