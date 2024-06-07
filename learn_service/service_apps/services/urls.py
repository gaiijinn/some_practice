from django.urls import path
from .views import SubscriptionReadOnlyViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path

app_name = 'services'

router = DefaultRouter()
router.register('subscription', SubscriptionReadOnlyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
