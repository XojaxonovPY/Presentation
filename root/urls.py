from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from root.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('ckeditor/', include('ckeditor_uploader.urls'))

]
urlpatterns += i18n_patterns(
    path('api/v1/', include('apps.urls'))
)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
