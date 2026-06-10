# dict/security_utils.py
import secrets
import hashlib
import base64
from cryptography.fernet import Fernet
from django.conf import settings

class SecurityUtils:
    """Security utility functions"""
    
    @staticmethod
    def generate_secure_token(length=32):
        """Generate a cryptographically secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_data(data):
        """Hash sensitive data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def encrypt_sensitive_data(data):
        """Encrypt sensitive data (like API keys) before storing"""
        # Generate a key from SECRET_KEY
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        cipher = Fernet(base64.urlsafe_b64encode(key))
        return cipher.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data):
        """Decrypt sensitive data"""
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        cipher = Fernet(base64.urlsafe_b64encode(key))
        return cipher.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def sanitize_input(data):
        """Sanitize user input to prevent XSS"""
        import html
        if isinstance(data, str):
            return html.escape(data.strip())
        elif isinstance(data, dict):
            return {k: SecurityUtils.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityUtils.sanitize_input(item) for item in data]
        return data