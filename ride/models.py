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
    request_time = models.TimeField(default=timezone.now)
    request_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # وضعیت درخواست (فعال یا قبول‌شده/منقضی)

    def __str__(self):
        return f"{self.passenger.full_name} - {self.request_type}"



