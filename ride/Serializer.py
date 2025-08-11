from rest_framework import serializers
from .models import RideRequest

class RideRequestSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source='passenger.name', read_only=True)

    class Meta:
        model = RideRequest
        fields = [
            'id', 'passenger_name', 'origin', 'destination',
            'request_type', 'is_hurry', 'scheduled_time',
            'status', 'created_at'
        ]
