from rest_framework import serializers
from .models import TripRequest, DriverQueue, DriverAcceptance

class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = '__all__'  # همه فیلدهای مدل
        # هیچ فیلدی read_only نیست مگر بخوای passenger رو دستی ست کنی در view


class DriverQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverQueue
        fields = '__all__'
        read_only_fields = ['joined_at']


class DriverAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAcceptance
        fields = '__all__'
        read_only_fields = ['accepted_at']
