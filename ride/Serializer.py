# ride/serializers.py (فایل جدید)

from rest_framework import serializers
from .models import CurrentTripe, DriverQueue, AcceptedTrip, AcceptedTripTable
from users.models import User

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']

class DriverQueueSerializer(serializers.ModelSerializer):
    driver = UserBriefSerializer(read_only=True)
    class Meta:
        model = DriverQueue
        fields = ['id', 'driver', 'zone', 'joined_at', 'is_active']

class CurrentTripeSerializer(serializers.ModelSerializer):
    passenger = UserBriefSerializer(read_only=True)
    class Meta:
        model = CurrentTripe
        fields = ['id', 'passenger', 'request_type', 'origin', 'destination', 'request_time', 'request_date', 'is_active']

class AcceptedTripSerializer(serializers.ModelSerializer):
    driver = UserBriefSerializer(read_only=True)
    passenger = UserBriefSerializer(read_only=True)
    class Meta:
        model = AcceptedTrip
        fields = ['id', 'driver', 'passenger', 'request_type', 'zone', 'created_at', 'is_finished']

class AcceptedTripTableSerializer(serializers.ModelSerializer):
    driver = UserBriefSerializer(read_only=True)
    passenger = UserBriefSerializer(read_only=True)
    class Meta:
        model = AcceptedTripTable
        fields = ['id', 'driver', 'passenger', 'region', 'request_type', 'start_time', 'finish_time']
