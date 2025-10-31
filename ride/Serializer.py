from rest_framework import serializers
from .models import CurrentTripe, TableTripe

class CurrentTripeSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source='passenger.full_name', read_only=True)
    passenger_phone = serializers.CharField(source='passenger.phone_number', read_only=True)

    class Meta:
        model = CurrentTripe
        fields = '__all__'


class TableTripeSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source='passenger.full_name', read_only=True)
    passenger_phone = serializers.CharField(source='passenger.phone_number', read_only=True)

    class Meta:
        model = TableTripe
        fields = '__all__'