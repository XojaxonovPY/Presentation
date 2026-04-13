from django.urls import path

from apps.views import SprintListAPIView, ProductListAPIView, FeatureListAPIView

urlpatterns = [
    path('sprints/', SprintListAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('features/', FeatureListAPIView.as_view())
]
