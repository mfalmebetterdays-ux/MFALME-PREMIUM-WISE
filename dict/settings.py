# dict/settings.py
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# ==============================
# BASE DIRECTORY
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# ENVIRONMENT DETECTION - FIXED!
# ==============================
# Check if running locally (Windows or local dev)
IS_RUNNING_LOCALLY = 'runserver' in sys.argv or 'localhost' in sys.argv or '127.0.0.1' in sys.argv

# Production detection - ONLY true on Railway/Render
IS_PRODUCTION = (os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or 
                os.environ.get('ON_RENDER') == 'true' or
                os.environ.get('DATABASE_URL', '').startswith('postgres://') and not IS_RUNNING_LOCALLY)

# Force production detection off for local development
if IS_RUNNING_LOCALLY:
    IS_PRODUCTION = False

IS_LOCAL = not IS_PRODUCTION

# ==============================
# CORE SETTINGS
# ==============================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key-for-local-only")

# Debug mode - ALWAYS False in production
if IS_PRODUCTION:
    DEBUG = False
    print("🔒 PRODUCTION: Debug mode is FORCED OFF for security")
else:
    DEBUG = True
    print("🔧 LOCAL DEVELOPMENT: Debug mode enabled")

# Allowed hosts for both environments
ALLOWED_HOSTS = [
    "tradewise.up.railway.app",
    "127.0.0.1",
    "localhost",
    "tradewise-hub.com",
    "www.tradewise-hub.com",
    ".railway.app",
    ".onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://tradewise.up.railway.app",
    "https://*.railway.app",
    "https://tradewise-hub.com",
    "https://www.tradewise-hub.com",
    "https://*.onrender.com",
]

# ==============================
# SECURITY MIDDLEWARE (Fixed)
# ==============================

class SecurityHeadersMiddleware:
    """Add comprehensive security headers to all responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
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
        if IS_PRODUCTION:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class BlockMaliciousBotsMiddleware:
    """Block known malicious bots and user agents"""
    
    BAD_USER_AGENTS = [
        r'sqlmap', r'nmap', r'nikto', r'nessus', r'burp', r'zap',
        r'wpscan', r'joomscan', r'dirb', r'gobuster', r'hydra',
        r'masscan', r'zgrab', r'httpx', r'nuclei', r'shodan',
        r'python-requests', r'python-urllib', r'curl', r'wget',
        r'Masscan', r'ZmEu', r'Morfeus', r'SiteGuard', r'Go-http-client'
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        import re
        from django.http import HttpResponseForbidden
        
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        for bad_agent in self.BAD_USER_AGENTS:
            if re.search(bad_agent, user_agent):
                # Log the blocked request
                print(f"🔴 BLOCKED Malicious Bot: {user_agent[:50]} from {request.META.get('REMOTE_ADDR')}")
                return HttpResponseForbidden("Access Denied")
        
        return self.get_response(request)


class IPWhitelistMiddleware:
    """Only allow specific IPs for admin panel"""
    
    # Add your trusted IPs here (admin IPs)
    TRUSTED_IPS = [
        '127.0.0.1',  # Local
        # Add your home/office IP addresses here
        # '102.0.0.1',  # Example: Your office IP
        # '105.0.0.1',  # Example: Your home IP
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        from django.http import HttpResponseForbidden
        
        # Only restrict admin and django admin panels in production
        if IS_PRODUCTION and (request.path.startswith('/admin/') or request.path.startswith('/dashboard/')):
            client_ip = self.get_client_ip(request)
            
            # Check if IP is whitelisted
            if client_ip not in self.TRUSTED_IPS:
                print(f"🔴 BLOCKED Unauthorized admin access from IP: {client_ip}")
                return HttpResponseForbidden("Admin access restricted")
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SQLInjectionBlocker:
    """Block SQL injection attempts"""
    
    SQL_PATTERNS = [
        r'union.*select', r'select.*from', r'insert.*into', r'delete.*from',
        r'drop.*table', r'create.*table', r'alter.*table', r'update.*set',
        r'--', r';\s*--', r'/\*.*\*/', r'xp_cmdshell', r'exec\s+sp_',
        r'char\s*\(\d+\)', r'@@version', r'database\(\)', r'user\(\)'
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        import re
        from django.http import HttpResponseNotFound
        
        # Check GET parameters
        for key, value in request.GET.items():
            if self.has_sql_injection(str(value)):
                print(f"🔴 SQL Injection blocked in GET: {key}={str(value)[:50]}")
                return HttpResponseNotFound()
        
        # Check POST parameters
        for key, value in request.POST.items():
            if self.has_sql_injection(str(value)):
                print(f"🔴 SQL Injection blocked in POST: {key}={str(value)[:50]}")
                return HttpResponseNotFound()
        
        return self.get_response(request)
    
    def has_sql_injection(self, text):
        import re
        text_lower = text.lower()
        for pattern in self.SQL_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False


class RateLimitMiddleware:
    """Advanced rate limiting with different limits for different endpoints"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        from django.core.cache import cache
        from django.http import JsonResponse
        
        # Only rate limit in production
        if not IS_PRODUCTION:
            return self.get_response(request)
        
        client_ip = self.get_client_ip(request)
        path = request.path
        
        # Different rate limits for different endpoints
        if path.startswith('/admin/'):
            limit = 30  # 30 requests per minute for admin
        elif path.startswith('/login/') or path.startswith('/signup/'):
            limit = 10  # 10 login attempts per minute
        else:
            limit = 100  # 100 requests per minute for regular users
        
        cache_key = f'rate_limit_{client_ip}_{path}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= limit:
            print(f"🔴 RATE LIMITED: {client_ip} exceeded {limit} requests on {path}")
            return JsonResponse(
                {'error': 'Too many requests. Please try again later.'},
                status=429
            )
        
        cache.set(cache_key, request_count + 1, 60)
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SessionSecurityMiddleware:
    """Enhance session security - FIXED: Added hasattr check"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        from django.http import JsonResponse
        from django.contrib.auth import logout
        
        # CRITICAL FIX: Check if user attribute exists before accessing
        # This prevents AttributeError when authentication middleware hasn't run yet
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if IP changed
            current_ip = self.get_client_ip(request)
            session_ip = request.session.get('ip_address')
            
            if session_ip and session_ip != current_ip:
                # Possible session hijacking
                print(f"🔴 Session IP mismatch: {session_ip} vs {current_ip}")
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
                logout(request)
                request.session.flush()
                return JsonResponse({'error': 'Session expired. Please login again.'}, status=401)
            
            request.session['user_agent'] = current_ua
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlockSuspiciousPathsMiddleware:
    """Middleware to block malicious scanner paths"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        import re
        # Compile patterns once for performance
        self.blocked_patterns = [
            r'\.env', r'wp-config', r'\.git', r'\.svn', r'\.hg',
            r'config\.json', r'credentials', r'\.pypirc', r'pip\.conf',
            r'backup.*\.sql', r'database\.sql', r'dump\.sql', 
            r'\.yaml$', r'\.yml$', r'xmlrpc\.php', r'server-status',
            r'api/docs', r'swagger', r'graphql', r'\.well-known',
            r'Procfile', r'Dockerfile', r'\.aws/', r'\.vscode/',
            r'\.terraform', r'\.netlify', r'\.vercel', r'\.circleci',
            r'Jenkinsfile', r'\.gitlab-ci\.yml', r'bitbucket-pipelines\.yml',
            r'\.github/', r'buildspec\.', r'cloudbuild\.', r'\.sh_history',
            r'\.zsh_history', r'debug/pprof', r'server/info', r'me$',
            r'admin/check', r'version$', r'\.git-credentials', r'\.netrc',
            r'\.DS_Store', r'\.git/config', r'\.env\.local', r'\.env\.production'
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.blocked_patterns]
        
    def __call__(self, request):
        from django.http import HttpResponseNotFound
        
        path = request.path.lower()
        
        # Check if path matches any blocked pattern
        for pattern in self.compiled_patterns:
            if pattern.search(path):
                # Block the request immediately
                return HttpResponseNotFound()
        
        return self.get_response(request)


# ==============================
# MIDDLEWARE CONFIGURATION - CRITICAL FIXED ORDER!
# ==============================
# IMPORTANT: Django's auth middleware MUST run before any custom middleware 
# that accesses request.user

MIDDLEWARE = [
    # Django core middleware (must come first in this order)
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Session and auth middleware - these add user attribute to request
    "django.contrib.sessions.middleware.SessionMiddleware",  # Required for auth
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # CRITICAL: Adds user to request
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # Custom security middleware (now safe to access request.user)
    "dict.settings.SessionSecurityMiddleware",  # Now has request.user available
    "dict.settings.BlockSuspiciousPathsMiddleware",
    "dict.settings.SecurityHeadersMiddleware",
    "dict.settings.BlockMaliciousBotsMiddleware",
    "dict.settings.SQLInjectionBlocker",
    "dict.settings.RateLimitMiddleware",
    "dict.settings.IPWhitelistMiddleware",
]

# ==============================
# DATABASE - SQLite locally, PostgreSQL in production
# ==============================
DATABASE_URL = os.environ.get('DATABASE_URL')

if IS_PRODUCTION and DATABASE_URL:
    # PRODUCTION: Use PostgreSQL from Railway/Render
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=300,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
    # Add connection pool options for production
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 5,
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
    }
    print("✅ PRODUCTION: Using PostgreSQL Database")
elif IS_PRODUCTION and not DATABASE_URL:
    # Production but no DATABASE_URL - fallback to SQLite (not recommended)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("⚠️  PRODUCTION WARNING: No DATABASE_URL found, using SQLite (not recommended)")
else:
    # LOCAL DEVELOPMENT: Use SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("✅ LOCAL: Using SQLite Database")

# ==============================
# LOGGING - Reduce noise in production
# ==============================
if IS_PRODUCTION:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',  # Only show warnings and errors
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'myapp': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }
else:
    # Local development - show all logs
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }

# ==============================
# PAYSTACK CONFIGURATION
# ==============================
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY", "")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY", "")

# ==============================
# APPLICATION DEFINITION
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary (only used in production)
    "cloudinary",
    "cloudinary_storage",

    "myapp",
]

ROOT_URLCONF = "dict.urls"
WSGI_APPLICATION = "dict.wsgi.application"

# ==============================
# ERROR HANDLERS
# ==============================
handler404 = 'myapp.views.handler404'
handler500 = 'myapp.views.handler500'
handler403 = 'myapp.views.handler403'
handler400 = 'myapp.views.handler400'

# ==============================
# TEMPLATES
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "myapp.context_processors.paystack_keys",
            ],
        },
    },
]

# ==============================
# EMAIL CONFIGURATION
# ==============================
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "theofficialtradewise@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

if EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = "TradeWise <theofficialtradewise@gmail.com>"
    SERVER_EMAIL = "TradeWise <theofficialtradewise@gmail.com>"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ==============================
# STATIC FILES
# ==============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

if IS_PRODUCTION:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    WHITENOISE_ALLOW_ALL_ORIGINS = False
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    WHITENOISE_ALLOW_ALL_ORIGINS = True

WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

# ==============================
# MEDIA FILES (LOCAL VS CLOUDINARY)
# ==============================
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if IS_PRODUCTION:
    # Production: Use Cloudinary
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
        "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    print("☁️  PRODUCTION: Cloudinary media storage enabled")
else:
    # Local: Use filesystem
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    print("📁 LOCAL: Using filesystem media storage")

# ==============================
# ENHANCED SECURITY SETTINGS
# ==============================

# Session security
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CSRF settings
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = True

# SSL/HTTPS Security (Production only)
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Data upload security
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
DATA_UPLOAD_MAX_NUMBER_FILES = 50

# Security email alerts (Add your email for security notifications)
ADMINS = [('Admin', 'admin@tradewise-hub.com')]
MANAGERS = ADMINS

# ==============================
# AUTH
# ==============================
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# ==============================
# INTERNATIONALIZATION
# ==============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# ==============================
# DEFAULT AUTO FIELD
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# CACHING - For rate limiting (production only)
# ==============================
if IS_PRODUCTION:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# ==============================
# ROBOTS.TXT HANDLING
# ==============================
# Create a simple robots.txt view if file doesn't exist
def robots_txt_view(request):
    from django.http import HttpResponse
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Allow: /",
        "Sitemap: https://tradewise.up.railway.app/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Add robots.txt URL pattern (will be in urls.py)
# In your urls.py, add: path('robots.txt', lambda request: HttpResponse(...))

# ==============================
# FINAL SETTINGS SUMMARY
# ==============================
print("=" * 50)
print("🚀 SETTINGS LOADED SUCCESSFULLY")
print(f"🌍 ENVIRONMENT: {'PRODUCTION' if IS_PRODUCTION else 'LOCAL DEVELOPMENT'}")
print(f"🐛 DEBUG: {DEBUG}")
print(f"🗄️ DATABASE: {'PostgreSQL' if IS_PRODUCTION and DATABASE_URL else 'SQLite'}")
print(f"📦 STATIC FILES: {STATICFILES_STORAGE}")
print(f"🛡️  Security Middleware: {'ENABLED' if IS_PRODUCTION else 'PARTIALLY ENABLED'}")
print(f"🔐 Session Security: {'ENABLED' if IS_PRODUCTION else 'ENABLED'}")
print(f"🚦 Rate Limiting: {'ENABLED' if IS_PRODUCTION else 'DISABLED'}")
print("=" * 50)