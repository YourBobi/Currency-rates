from full_rest_api.nbrb.views import CatalogCompanyLinkViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)

app_name = 'nbrb'

router.register(
    '',
    CatalogCompanyLinkViewSet,
    basename='CatalogCompanyLinkViewSet',
)


urlpatterns = router.urls
