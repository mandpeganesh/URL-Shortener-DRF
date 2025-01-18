from django.db import models
from django.utils import timezone
from datetime import timedelta


class ShortenedURL(models.Model):
    """
    ShortenedURL model
    """
    original_url = models.URLField(max_length=2048)
    short_url = models.URLField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_url

    @property
    def is_expired(self):
        return timezone.now() > self.expired_at
    

class AccessLog(models.Model):
    """
    AccessLog model
    """
    url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='access_logs')
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    

    class Meta:
        ordering = ['-accessed_at']