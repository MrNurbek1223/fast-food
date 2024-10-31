from django_filters import rest_framework as filters

from app.food.api.food.models import FoodItem


class FoodItemFilter(filters.FilterSet):
    branch_id = filters.NumberFilter(field_name="branch__id", lookup_expr="exact")

    class Meta:
        model = FoodItem
        fields = ['branch_id', 'category']
