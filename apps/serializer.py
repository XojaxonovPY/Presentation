from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.models import Sprint, Product, Feature, FeatureFile


class SprintModelSerializer(ModelSerializer):
    features_count = SerializerMethodField()

    class Meta:
        model = Sprint
        fields = '__all__'

    def get_features_count(self, obj):
        return obj.features.count()


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FeatureFileModelSerializer(ModelSerializer):
    class Meta:
        model = FeatureFile
        fields = '__all__'


class FeatureModelSerializer(ModelSerializer):
    features_files = FeatureFileModelSerializer(many=True, read_only=True)
    sprint_name = ReadOnlyField(source='sprint.name')
    product_title = ReadOnlyField(source='product.title')

    class Meta:
        model = Feature
        fields = "__all__"
        extra_kwargs = {
            'sprint': {'write_only': True},
            'product': {'write_only': True}
        }
