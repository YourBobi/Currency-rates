
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^', include('full_rest_api.urls', namespace='api')),
]
