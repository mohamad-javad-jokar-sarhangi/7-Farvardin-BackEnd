from rest_framework import serializers
from .models import TripRequest

class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = '__all__'  # همه فیلدهای مدل
        # هیچ فیلدی read_only نیست مگر بخوای passenger رو دستی ست کنی در view


