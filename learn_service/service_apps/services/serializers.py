from rest_framework.serializers import ModelSerializer
from .models import Subscription


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        models = Subscription
        fields = '__all__'
