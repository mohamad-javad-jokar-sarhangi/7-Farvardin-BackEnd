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
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES, default='normal')  # نوع درخواست
    request_time = models.DateTimeField(auto_now_add=True)  # زمان درخواست
    
    
     # ➜ فیلد جدید برای راننده‌ای که درخواست را قبول کرده
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_trips'
    )
    
    def __str__(self):
        return f"{self.passenger_name} - {self.origin} to {self.destination}"


class DriverQueue(models.Model):
    DIRECTION_CHOICES = [
        ('روستا به شهر', 'روستا به شهر'),
        ('شهر به روستا', 'شهر به روستا'),
    ]

    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'راننده'})
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.driver.name} ({self.get_direction_display()})"