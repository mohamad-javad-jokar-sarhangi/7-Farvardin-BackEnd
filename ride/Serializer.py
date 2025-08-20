from rest_framework import serializers
from .models import TripRequest, DriverQueue, DriverAcceptance

class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = '__all__'
        read_only_fields = ['status', 'created_at']


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
