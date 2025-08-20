from django.db import models

from django.db import models


class TripRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('instant', 'درخواست فوری'),
        ('scheduled', 'درخواست زمان‌بندی شده'),
        ('vip', 'درخواست دربست'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('go', 'رفت'),
        ('return', 'برگشت'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید راننده'),
        ('accepted', 'پذیرفته شده'),
        ('cancelled', 'لغو شده'),
        ('completed', 'انجام شده'),
    ]

    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='trip_requests')
    driver = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_trips')
    neighborhood = models.CharField(max_length=255)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)
    is_hurry = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_time = models.DateTimeField(null=True, blank=True)  # فقط وقتی request_type = scheduled
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"درخواست {self.passenger.name} - {self.get_request_type_display()}"

