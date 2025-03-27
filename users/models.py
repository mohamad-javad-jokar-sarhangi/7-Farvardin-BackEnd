from django.db import models

# مدل کاربران ثبت نشده
class UserNotRegister(models.Model):
    name = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    role = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

# مدل کاربران نهایی
class User(models.Model):
    name = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    role = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name
