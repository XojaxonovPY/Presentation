from modeltranslation.translator import TranslationOptions, register

from apps.models import Sprint, Product, Feature


@register(Sprint)
class SprintTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', "description")
