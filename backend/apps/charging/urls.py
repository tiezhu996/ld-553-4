from rest_framework.routers import DefaultRouter
from apps.charging.views import ChargingPileViewSet, ChargingRecordViewSet

router = DefaultRouter()
router.register("", ChargingPileViewSet, basename="charging-piles")
router.register("records", ChargingRecordViewSet, basename="charging-records")
urlpatterns = router.urls
