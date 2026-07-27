from django.urls import path

from apps.views import SprintListAPIView, ProductListAPIView, FeatureListAPIView, PresentationTemplateView

urlpatterns = [

    path('sprints/', SprintListAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('features/', FeatureListAPIView.as_view()),
    path("main/", PresentationTemplateView.as_view())
]
