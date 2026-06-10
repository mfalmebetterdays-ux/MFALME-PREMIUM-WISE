# dict/security_middleware.py
import re
import hashlib
import time
from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from ipaddress import ip_address, ip_network

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add comprehensive security headers to all responses"""
    
    def process_response(self, request, response):
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove Server header
        if 'Server' in response:
            del response['Server']
        
        # Add security headers for HTTPS (production only)
        if not request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class BlockMaliciousBotsMiddleware(MiddlewareMixin):
    """Block known malicious bots and user agents"""
    
    BAD_USER_AGENTS = [
        r'sqlmap', r'nmap', r'nikto', r'nessus', r'burp', r'zap',
        r'wpscan', r'joomscan', r'dirb', r'gobuster', r'hydra',
        r'masscan', r'zgrab', r'httpx', r'nuclei', r'shodan',
        r'python-requests', r'python-urllib', r'curl', r'wget',
        r'Masscan', r'ZmEu', r'Morfeus', r'SiteGuard', r'Go-http-client'
    ]
    
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        for bad_agent in self.BAD_USER_AGENTS:
            if re.search(bad_agent, user_agent):
                # Log the blocked request
                print(f"🔴 BLOCKED Malicious Bot: {user_agent[:50]} from {request.META.get('REMOTE_ADDR')}")
                return HttpResponseForbidden("Access Denied")
        
        return None


class IPWhitelistMiddleware(MiddlewareMixin):
    """Only allow specific IPs for admin panel"""
    
    # Add your trusted IPs here (admin IPs)
    TRUSTED_IPS = [
        '127.0.0.1',  # Local
        # Add your home/office IP addresses here
        # '102.0.0.1',  # Example: Your office IP
        # '105.0.0.1',  # Example: Your home IP
    ]
    
    def process_request(self, request):
        # Only restrict admin and django admin panels
        if request.path.startswith('/admin/') or request.path.startswith('/dashboard/'):
            client_ip = self.get_client_ip(request)
            
            # Skip whitelist check for development
            from django.conf import settings
            if settings.DEBUG:
                return None
            
            # Check if IP is whitelisted
            if client_ip not in self.TRUSTED_IPS:
                print(f"🔴 BLOCKED Unauthorized admin access from IP: {client_ip}")
                return HttpResponseForbidden("Admin access restricted")
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SQLInjectionBlocker(MiddlewareMixin):
    """Block SQL injection attempts"""
    
    SQL_PATTERNS = [
        r'union.*select', r'select.*from', r'insert.*into', r'delete.*from',
        r'drop.*table', r'create.*table', r'alter.*table', r'update.*set',
        r'--', r';\s*--', r'/\*.*\*/', r'xp_cmdshell', r'exec\s+sp_',
        r'char\s*\(\d+\)', r'@@version', r'database\(\)', r'user\(\)'
    ]
    
    def process_request(self, request):
        # Check GET parameters
        for key, value in request.GET.items():
            if self.has_sql_injection(str(value)):
                print(f"🔴 SQL Injection blocked in GET: {key}={value[:50]}")
                return HttpResponseNotFound()
        
        # Check POST parameters
        for key, value in request.POST.items():
            if self.has_sql_injection(str(value)):
                print(f"🔴 SQL Injection blocked in POST: {key}={value[:50]}")
                return HttpResponseNotFound()
        
        return None
    
    def has_sql_injection(self, text):
        text_lower = text.lower()
        for pattern in self.SQL_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False


class RateLimitMiddleware(MiddlewareMixin):
    """Advanced rate limiting with different limits for different endpoints"""
    
    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        path = request.path
        
        # Different rate limits for different endpoints
        if path.startswith('/admin/'):
            limit = 30  # 30 requests per minute for admin
            block_duration = 300  # Block for 5 minutes
        elif path.startswith('/login/') or path.startswith('/signup/'):
            limit = 10  # 10 login attempts per minute
            block_duration = 900  # Block for 15 minutes
        else:
            limit = 100  # 100 requests per minute for regular users
            block_duration = 60  # Block for 1 minute
        
        cache_key = f'rate_limit_{client_ip}_{path}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= limit:
            print(f"🔴 RATE LIMITED: {client_ip} exceeded {limit} requests on {path}")
            return JsonResponse(
                {'error': 'Too many requests. Please try again later.'},
                status=429
            )
        
        cache.set(cache_key, request_count + 1, 60)
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SessionSecurityMiddleware(MiddlewareMixin):
    """Enhance session security"""
    
    def process_request(self, request):
        # Check if session is valid
        if request.user.is_authenticated:
            # Check if IP changed
            current_ip = self.get_client_ip(request)
            session_ip = request.session.get('ip_address')
            
            if session_ip and session_ip != current_ip:
                # Possible session hijacking
                print(f"🔴 Session IP mismatch: {session_ip} vs {current_ip}")
                from django.contrib.auth import logout
                logout(request)
                request.session.flush()
                return JsonResponse({'error': 'Session expired. Please login again.'}, status=401)
            
            # Store current IP in session
            request.session['ip_address'] = current_ip
            
            # Check user agent
            current_ua = request.META.get('HTTP_USER_AGENT', '')
            session_ua = request.session.get('user_agent')
            
            if session_ua and session_ua != current_ua:
                print(f"🔴 User Agent changed: possible session hijacking")
                from django.contrib.auth import logout
                logout(request)
                request.session.flush()
                return JsonResponse({'error': 'Session expired. Please login again.'}, status=401)
            
            request.session['user_agent'] = current_ua
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip