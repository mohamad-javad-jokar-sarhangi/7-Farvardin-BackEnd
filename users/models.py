from django.db import models

# مدل کاربران ثبت نشده
class UserNotRegister(models.Model):
    name = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    role = models.CharField(max_length=50, blank=False)
    location = models.CharField(max_length=50, default="نامشخص", blank=False)

    def __str__(self):
        return self.name

# مدل کاربران نهایی

class User(models.Model):
    ROLE_CHOICES = [
        ('مسافر', 'مسافر'),
        ('راننده', 'راننده'),
        ('فروشنده', 'فروشنده'),
        ('دهیار', 'دهیار'),
        ('شورا', 'شورا'),
    ]

    name = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    location = models.CharField(max_length=50, default="نامشخص", blank=False)

    def __str__(self):
        return self.name

    @property
    def is_driver(self):
        return self.role == 'driver'

