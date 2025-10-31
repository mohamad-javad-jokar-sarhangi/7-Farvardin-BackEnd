from django.db import models
from django.utils import timezone
from users.models import User

REQUEST_TYPE_CHOICES = [
    ('normal', 'Normal'),
    ('hurryup', 'Hurry Up'),
    ('vip', 'VIP'),
]

class CurrentTripe(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_tripes')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES, default='normal')
    origin = models.CharField(max_length=50)       # ✅ مبدا
    destination = models.CharField(max_length=50)  # ✅ مقصد
    request_time = models.TimeField(default=timezone.now)
    request_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # وضعیت درخواست (فعال یا قبول‌شده/منقضی)

    def __str__(self):
        return f"{self.passenger.full_name} - {self.request_type}"

def current_time():
    return timezone.now().time()

class TableTripe(models.Model):
    passenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'مسافر'},
        related_name='table_tripes'
    )
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    request_date = models.DateField(default=timezone.now)
    request_time = models.TimeField(default=current_time)

    def __str__(self):
        return f"{self.passenger.name} از {self.origin} به {self.destination}"

REQUEST_TYPE_CHOICES = [
    ('normal', 'Normal'),
    ('hurryup', 'Hurry Up'),
    ('vip', 'VIP'),
]

ZONE_CHOICES = [
    ('city', 'شهر'),
    ('village', 'روستا'),
]


class DriverQueue(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'راننده'})
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # اگر حرکت کرده false میشه

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.driver.name} ({self.zone})"


class AcceptedTrip(models.Model):

    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'راننده'},
        related_name='accepted_driver_trips'   # ← اضافه شد
    )
    passenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'مسافر'},
        related_name='accepted_passenger_trips'  # ← اضافه شد
    )
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES)


    def __str__(self):
        return f"{self.driver.name} => {self.passenger.name} ({self.request_type})"
    
    
    
    
    
    
    
    
    