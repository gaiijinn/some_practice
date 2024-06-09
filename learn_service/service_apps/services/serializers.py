from rest_framework import serializers

from .models import Plan, Service, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.company_name')
    client_email = serializers.EmailField(source='client.user.email')
    service_name = serializers.CharField(source='service.name')
    service_raw_price = serializers.CharField(source='service.full_price')
    price = serializers.SerializerMethodField()

    plan = PlanSerializer()

    def get_price(self, instance):
        return instance.price

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'client_email', 'service_name', 'service_raw_price', 'plan', 'price')
