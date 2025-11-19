from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_otp = models.CharField(max_length=6, null= True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    
    def is_otp_expired(self):
        if not self.otp_created_at:
            return True
        
        return timezone.now() > self.otp_created_at+timedelta(minutes=2)
    
    def otp_cooldown(self):
        if not self.otp_created_at:
            return True
        return timezone.now() < self.otp_created_at + timezone.timedelta(seconds=30)