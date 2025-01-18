from django.contrib import admin
from .models import ShortenedURL, AccessLog


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ['original_url', 'short_url', 'created_at', 'expired_at', 'is_active', 'is_expired']
    list_filter = ['created_at', 'expired_at', 'is_active']
    search_fields = ['original_url', 'short_url']
    readonly_fields = ['created_at',]
    ordering = ['-created_at']
    

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['url', 'accessed_at', 'ip_address']
    list_filter = ['accessed_at']
    search_fields = ['url__original_url', 'ip_address']
    ordering = ['-accessed_at']
