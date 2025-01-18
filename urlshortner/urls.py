from django.contrib import admin
from django.urls import path, include
from shortener.views import URLShortenerViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shorten/', URLShortenerViewSet.as_view({'post': 'create'})),
    path('api/v1/urls/<str:short_url>/', URLShortenerViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/urls/<str:short_url>/analytics/', URLShortenerViewSet.as_view({'get': 'analytics'})),
]