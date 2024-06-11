"""Public swagger patterns."""

from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


app_name = "public_swagger"

patterns_for_schema = []


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(urlconf=patterns_for_schema), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='public_swagger:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='public_swagger:schema'), name='redoc'),
]
