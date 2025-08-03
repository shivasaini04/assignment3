from dataclasses import dataclass
from typing import Optional
import re
import hashlib
import os

@dataclass
class User:
    name: str
    email: str
    password: str
    id: Optional[int] = None

    def validate(self):
        errors = []
        
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not self.email or not email_pattern.match(self.email):
            errors.append("Invalid email format")
            
        if not self.password or len(self.password) < 8:
            errors.append("Password must be at least 8 characters long")
            
        return errors

    def hash_password(self):
        """Hash the password with a random salt"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            self.password.encode('utf-8'),
            salt,
            100000
        )
        return salt + key

    @staticmethod
    def verify_password(stored_password: bytes, provided_password: str) -> bool:
        """Verify a stored password against one provided by user"""
        salt = stored_password[:32]
        stored_key = stored_password[32:]
        provided_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        return stored_key == provided_key
