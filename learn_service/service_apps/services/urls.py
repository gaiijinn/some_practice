from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionReadOnlyViewSet

app_name = 'services'

router = DefaultRouter()
router.register('subscription', SubscriptionReadOnlyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
