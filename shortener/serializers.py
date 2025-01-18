from rest_framework import serializers
from .models import ShortenedURL, AccessLog


class ShortenedURLSerializer(serializers.ModelSerializer):
    """
    Serializer for ShortenedURL model
    """
    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_url', 'created_at', 'expired_at', 'password']
        read_only_fields = ['short_url', 'created_at']
        extra_kwargs = {
            'expired_at': {'read_only': True},
            'password': {'required': False},
        }
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return obj.short_url
        return request.build_absolute_uri(f'/api/v1/urls/{obj.short_url}/')

class AccessLogSerializer(serializers.ModelSerializer):
    """
    Serializer for AccessLog model
    """
    class Meta:
        model = AccessLog
        fields = ['accessed_at', 'ip_address']
        

class AnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for Analytics
    """
    access_logs = AccessLogSerializer(many=True, read_only=True)
    access_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_url', 'created_at', 'expired_at', 'access_count', 'access_logs']
        
    def get_access_count(self, obj):
        return obj.access_logs.count()