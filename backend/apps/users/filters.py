from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    email_start = filters.CharFilter('email', 'istartswith')
    email_contains = filters.CharFilter('email', 'icontains')
    name_contains = filters.CharFilter(field_name='profile__name', lookup_expr='icontains')
    name_start = filters.CharFilter(field_name='profile__name', lookup_expr='istartswith')
    surname_contains = filters.CharFilter(field_name='profile__surname', lookup_expr='icontains')
    surname_start = filters.CharFilter(field_name='profile__surname', lookup_expr='istartswith')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'email',
            ('profile__name', 'name'),
            ('profile__surname', 'surname'),
            ('profile__age', 'age'),
        )
    )

