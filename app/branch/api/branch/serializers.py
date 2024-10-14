from rest_framework import serializers
from app.branch.api.branch.models import Branch
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from page.models import User
from rest_framework_gis.serializers import GeoFeatureModelSerializer



class BranchSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='branch_admin'))
    class Meta:
        geo_field = "location"
        model = Branch
        fields = ['id', 'name', 'image', 'description', 'address','admin']