from django_filters import rest_framework as filters
from .models import Ad


class AdFilters(filters.FilterSet):
    keyword = filters.CharFilter(field_name='title', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price' or 0, lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price' or 10000000, lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ['category', 'min_price', 'max_price', 'keyword']