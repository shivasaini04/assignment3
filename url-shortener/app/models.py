from datetime import datetime
import random
import string
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class URLMapping:
    original_url: str
    short_code: str
    created_at: datetime
    clicks: int = 0

class URLStore:
    def __init__(self):
        self._urls: Dict[str, URLMapping] = {}

    def create_short_code(self) -> str:
        """Generate a random 6-character alphanumeric code"""
        while True:
            # Generate a random 6-character code
            chars = string.ascii_letters + string.digits
            code = ''.join(random.choice(chars) for _ in range(6))
            # Make sure it's unique
            if code not in self._urls:
                return code

    def add_url(self, url: str) -> URLMapping:
        """Add a new URL to the store"""
        short_code = self.create_short_code()
        mapping = URLMapping(
            original_url=url,
            short_code=short_code,
            created_at=datetime.utcnow()
        )
        self._urls[short_code] = mapping
        return mapping

    def get_url(self, short_code: str) -> Optional[URLMapping]:
        """Get a URL mapping by short code"""
        return self._urls.get(short_code)

    def increment_clicks(self, short_code: str) -> None:
        """Increment the click count for a URL"""
        if mapping := self._urls.get(short_code):
            mapping.clicks += 1

# Global URL store instance
url_store = URLStore()