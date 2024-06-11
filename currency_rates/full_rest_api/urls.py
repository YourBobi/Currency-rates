"""Public swagger patterns."""

from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

app_name = "public_swagger"

patterns_for_schema = [
    path('nbrb/', include('full_rest_api.nbrb.urls_public', 'nbrb')),
]


urlpatterns = patterns_for_schema + [
    path('schema/', SpectacularAPIView.as_view(urlconf=patterns_for_schema), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='public_swagger:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='public_swagger:schema'), name='redoc'),
]
