from django.db import models
from users.models import User

class TripRequest(models.Model):
    REQUEST_TYPES = [
        ('درخواست دربست', 'درخواست دربست'),
        ('درخواست عادی', 'درخواست عادی'),
        ('عجله دارم (حساب بقیه میکنم)', 'عجله دارم (حساب بقیه میکنم)'),
    ]
    passenger_name = models.CharField(max_length=100)   # اسم مسافر
    passenger_phone = models.CharField(max_length=20)   # شماره تماس
    origin = models.CharField(max_length=100)           # مبدأ (روستا)
    destination = models.CharField(max_length=100)      # مقصد (شهر)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_requests')
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES, default='normal')  # نوع درخواست

    def __str__(self):
        return f"{self.passenger_name} - {self.origin} to {self.destination}"


class DriverQueue(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queue_positions')
    queue_type = models.CharField(
        max_length=20,
        choices=[
            ('village', 'صف روستا'),
            ('city', 'صف شهر'),
        ]
    )
    location_name = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'joined_at']

    def __str__(self):
        return f"{self.driver} در {self.queue_type} - {self.location_name}"


class DriverAcceptance(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_trips')
    trip_request = models.OneToOneField(TripRequest, on_delete=models.CASCADE, related_name='driver_acceptance')
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver} → {self.trip_request}"


