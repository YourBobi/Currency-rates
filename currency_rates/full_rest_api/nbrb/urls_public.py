from full_rest_api.nbrb.views import CurrencyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)

app_name = 'nbrb'

router.register(
    '',
    CurrencyViewSet,
    basename='CurrencyViewSet',
)


urlpatterns = router.urls
