from django_filters import ModelChoiceFilter
from django_filters.rest_framework import FilterSet

from apps.models import Feature, Sprint, Product


class FeatureFilterSet(FilterSet):
    sprint = ModelChoiceFilter(queryset=Sprint.objects.all(), to_field_name='id')
    product = ModelChoiceFilter(queryset=Product.objects.all(), to_field_name='id')

    class Meta:
        model = Feature
        fields = ['sprint', 'product']
