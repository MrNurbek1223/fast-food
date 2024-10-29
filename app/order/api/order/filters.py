from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    branch_id = filters.NumberFilter(field_name="branch__id", required=True)
    status = filters.CharFilter(field_name="status", required=False)

    class Meta:
        model = Order
        fields = ['branch_id', 'status']
