from rest_framework import serializers
from app.branch.api.branch.models import Branch
from page.models import User
from django.contrib.gis.geos import Point


class BranchSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='branch_admin'))
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        geo_field = "location"
        model = Branch
        fields = ['id', 'name', 'image', 'description', 'address', 'admin', 'longitude', 'latitude']

    def validate(self, data):
        longitude = data.pop('longitude', None)
        latitude = data.pop('latitude', None)
        if longitude is not None and latitude is not None:
            data['location'] = Point(longitude, latitude, srid=4326)
        elif not self.instance:
            raise serializers.ValidationError("Filial joylashuvini to'liq kiriting.")
        return data

    def create(self, validated_data):
        location = validated_data.pop('location', None)
        branch = Branch.objects.create(**validated_data, location=location)
        return branch

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.location:
            representation['longitude'] = instance.location.x
            representation['latitude'] = instance.location.y
        return representation