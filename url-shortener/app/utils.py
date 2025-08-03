from urllib.parse import urlparse
from typing import Dict, Any
from .models import URLMapping

def validate_url(url: str) -> bool:
    """
    Validate if the given string is a proper URL.
    Returns True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def create_response(data: Dict[str, Any], status_code: int = 200) -> tuple[Dict[str, Any], int]:
    """Create a standardized API response"""
    return data, status_code

def format_url_data(base_url: str, mapping: 'URLMapping') -> Dict[str, Any]:
    """Format URL mapping data for API response"""
    return {
        'short_code': mapping.short_code,
        'short_url': f"{base_url}/{mapping.short_code}",
        'original_url': mapping.original_url,
        'clicks': mapping.clicks,
        'created_at': mapping.created_at.isoformat()
    }