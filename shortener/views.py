from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import redirect
from django.http import Http404
from django.utils import timezone
from .models import ShortenedURL, AccessLog
from .serializers import ShortenedURLSerializer, AnalyticsSerializer
from .utils import generate_short_url, get_expiration_time, is_valid_url
from django.contrib.auth.hashers import make_password, check_password


class URLShortenerViewSet(viewsets.ViewSet):
    def create(self, request):
        """
        Create a shortened URl
        """
        serializer = ShortenedURLSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        original_url = serializer.validated_data['original_url']
        expired_at = serializer.validated_data.get('expired_at', 24)
        password = serializer.validated_data.get('password')
        
        if not original_url or not is_valid_url(original_url):
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        short_url = generate_short_url(original_url)
        
        if password:
            password = make_password(password)
        
        try:
            shortened_url = ShortenedURL.objects.create(
                original_url=original_url,
                short_url=short_url,
                expired_at=get_expiration_time(expired_at),
                password=password
            )
            
            serializer = ShortenedURLSerializer(shortened_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error creating shortened url: {str(e)}'}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def retrieve(self, request, short_url=None):
        """
        Redirect to Original URL
        """
        try:
            url_obj = ShortenedURL.objects.get(short_url=short_url)
            
            if url_obj.is_expired:
                return Response({'error': 'URL has expired'},
                                status=status.HTTP_410_GONE)
            
            if url_obj.password:
                provided_password = request.query_params.get('password')
                
                if not provided_password or not check_password(provided_password, url_obj.password):
                    return Response({'error': 'Password required or Invalid'}, 
                                    status=status.HTTP_401_UNAUTHORIZED)
            
            # Log access
            AccessLog.objects.create(url=url_obj, 
                                     ip_address=request.META.get('REMOTE_ADDR', '0.0.0.0'))
            
            return redirect(url_obj.original_url)
        
        except ShortenedURL.DoesNotExist:
            raise Http404
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, short_url=None):
        """
        Get analytics for a specific URL
        """
        try:
            url_obj = ShortenedURL.objects.get(short_url=short_url)
            serializer = AnalyticsSerializer(url_obj)
            return Response(serializer.data)
        except ShortenedURL.DoesNotExist:
            raise Http404