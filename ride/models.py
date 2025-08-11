from django.db import models
from users.models import User

class RideRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('scheduled', 'شب قبل'),
        ('normal', 'عادی'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('accepted', 'تایید شده'),
        ('completed', 'انجام شده'),
        ('cancelled', 'لغو شده'),
    ]

    passenger = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ride_requests'
    )
    driver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_rides'
    )

    origin = models.CharField(max_length=100, default="نامشخص")       # مبدأ
    destination = models.CharField(max_length=100)  # مقصد
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES , default="نامشخص")
    is_hurry = models.BooleanField(default=False)  # اگه عجله داره
    scheduled_time = models.DateTimeField(null=True, blank=True)  # اگه شب قبل ثبت شده

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.name} - {self.origin} → {self.destination}"


class DriverQueue(models.Model):
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='queues'
    )
    location = models.CharField(max_length=100)  # مبدا یا مقصد صف
    position = models.PositiveIntegerField()     # رتبه در صف

    class Meta:
        unique_together = ('driver', 'location')  # هر راننده یکبار در صف خاص

    def __str__(self):
        return f"{self.driver.name} - {self.location} (رتبه: {self.position})"





