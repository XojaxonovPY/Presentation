from rest_framework.generics import ListAPIView

from apps.filters import FeatureFilterSet
from apps.models import Sprint, Product, Feature
from apps.serializer import SprintModelSerializer, ProductModelSerializer, FeatureModelSerializer


class SprintListAPIView(ListAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintModelSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class FeatureListAPIView(ListAPIView):
    queryset = Feature.objects.select_related('sprint', 'product').prefetch_related('features_files').all()
    serializer_class = FeatureModelSerializer
    filterset_class = FeatureFilterSet
