from rest_framework import serializers
from .models import TripRequest, DriverQueue

class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = '__all__'


class DriverQueueSerializer(serializers.ModelSerializer):
    driver_username = serializers.CharField(source='driver.username', read_only=True)

    class Meta:
        model = DriverQueue
        fields = ['id', 'driver', 'driver_username', 'direction', 'joined_at', 'is_active']
