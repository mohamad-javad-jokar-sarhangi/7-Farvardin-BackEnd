from rest_framework import serializers
from .models import UserNotRegister, User

# Serializer برای مدل کاربران ثبت نشده
class UserNotRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotRegister
        fields = '__all__'  # تمام فیلدهای مدل را در JSON قرار دهد
