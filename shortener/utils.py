import hashlib
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

# Generate short URL
def generate_short_url(url):
    hash_object = hashlib.md5(url.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:7]

# Generate expired time
def get_expiration_time(hours=24):
    return timezone.now() + timezone.timedelta(hours=hours)

# Check if URL is valid
def is_valid_url(url):
    validator = URLValidator()
    
    try:
        validator(url)
        return True
    except ValidationError:
        return False