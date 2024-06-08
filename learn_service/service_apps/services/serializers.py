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

    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'client_email', 'service_name', 'plan')
