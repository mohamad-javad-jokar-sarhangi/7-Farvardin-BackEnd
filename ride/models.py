from django.db import models

class TripRequest(models.Model):
    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='trip_requests')
    origin = models.CharField(max_length=255)      # نام روستای مسافر
    destination = models.CharField(max_length=255) # همیشه شهر (فعلاً یک شهر)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'در انتظار'),
            ('accepted', 'پذیرفته شده'),
            ('cancelled', 'لغو شده'),
            ('completed', 'انجام شده'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"درخواست {self.passenger} از {self.origin} به {self.destination}"


class DriverQueue(models.Model):
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='queue_positions')
    queue_type = models.CharField(   # village = آخرین روستا، city = شهر
        max_length=20,
        choices=[
            ('village', 'صف روستا'),
            ('city', 'صف شهر'),
        ]
    )
    location_name = models.CharField(max_length=255)  # نام آخرین روستا یا شهر
    position = models.PositiveIntegerField(default=0) # ترتیب ورود
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'joined_at']

    def __str__(self):
        return f"{self.driver} در {self.queue_type} - {self.location_name}"


class DriverAcceptance(models.Model):
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='accepted_trips')
    trip_request = models.OneToOneField(TripRequest, on_delete=models.CASCADE, related_name='driver_acceptance')
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver} → {self.trip_request}"
