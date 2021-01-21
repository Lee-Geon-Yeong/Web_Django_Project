import django_filters
from .models import Drinks, Brand


class DrinkFilter(django_filters.FilterSet):
    BRAND_CHOICES = tuple(
        (brand.name, brand.name) for brand in Brand.objects.all())
    name = django_filters.CharFilter(lookup_expr='icontains')
    price_lt = django_filters.NumberFilter(field_name='price',
                                           lookup_expr='lt')
    price_gt = django_filters.NumberFilter(field_name='price',
                                           lookup_expr='gt')
    brands = django_filters.MultipleChoiceFilter(field_name='brand__name',
                                                 choices=BRAND_CHOICES)
    o = django_filters.OrderingFilter(
        fields = ('likes', 'likes')
    )

    class Meta:
        model = Drinks
        fields = ['name', 'brands']


"""
f = F({'date_after': '2016-01-01', 'date_before': '2016-02-01'})
"""