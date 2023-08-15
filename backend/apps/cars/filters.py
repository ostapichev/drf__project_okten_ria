from django_filters import rest_framework as filters


class CarFilter(filters.FilterSet):
    year_lt = filters.NumberFilter('year', 'lt')
    year_gt = filters.NumberFilter('year', 'gt')
    year_range = filters.RangeFilter('year')
    year_in = filters.BaseInFilter('year')
    brand_contains = filters.CharFilter('brand', 'icontains')
    model_contains = filters.CharFilter('model', 'icontains')
    order = filters.OrderingFilter(
        fields={'id', 'brand', 'model', 'year', 'price'}
    )