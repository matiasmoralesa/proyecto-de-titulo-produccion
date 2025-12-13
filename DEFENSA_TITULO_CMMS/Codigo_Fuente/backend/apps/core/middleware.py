"""
Security and logging middleware for CMMS application
"""
import logging
import uuid
import time
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all requests with request ID for correlation
    """
    
    def process_request(self, request):
        # Generate unique request ID
        request.request_id = str(uuid.uuid4())
        request.start_time = time.time()
        
        # Log request
        logger.info(
            'Request started',
            extra={
                'request_id': request.request_id,
                'method': request.method,
                'path': request.path,
                'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                'ip': self.get_client_ip(request),
            }
        )
        
        return None
    
    def process_response(self, request, response):
        # Calculate request duration
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log response
            logger.info(
                'Request completed',
                extra={
                    'request_id': getattr(request, 'request_id', 'unknown'),
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2),
                    'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                }
            )
            
            # Add request ID to response headers
            response['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        
        return response
    
    def process_exception(self, request, exception):
        # Log exceptions
        logger.error(
            'Request failed with exception',
            extra={
                'request_id': getattr(request, 'request_id', 'unknown'),
                'method': request.method,
                'path': request.path,
                'exception': str(exception),
                'exception_type': type(exception).__name__,
            },
            exc_info=True
        )
        
        return None
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to all responses
    """
    
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data:; "
            "connect-src 'self' http://localhost:* http://127.0.0.1:*; "
            "frame-ancestors 'none';"
        )
        
        # Strict Transport Security (HSTS)
        # Only enable in production with HTTPS
        if not request.is_secure():
            # For development without HTTPS
            pass
        else:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options (already set by Django, but ensuring it)
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(), '
            'usb=(), '
            'magnetometer=(), '
            'gyroscope=(), '
            'accelerometer=()'
        )
        
        return response


class InputSanitizationMiddleware(MiddlewareMixin):
    """
    Middleware to sanitize input data
    """
    
    def process_request(self, request):
        # Sanitize query parameters
        if request.GET:
            sanitized_get = request.GET.copy()
            for key, value in sanitized_get.items():
                if isinstance(value, str):
                    # Remove potentially dangerous characters
                    sanitized_get[key] = self.sanitize_string(value)
            request.GET = sanitized_get
        
        return None
    
    @staticmethod
    def sanitize_string(value):
        """
        Basic sanitization of string input
        Remove script tags and other potentially dangerous content
        """
        import re
        
        # Remove script tags
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove iframe tags
        value = re.sub(r'<iframe[^>]*>.*?</iframe>', '', value, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove on* event handlers
        value = re.sub(r'\s*on\w+\s*=\s*["\']?[^"\']*["\']?', '', value, flags=re.IGNORECASE)
        
        return value


class RateLimitHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add rate limit information to response headers
    """
    
    def process_response(self, request, response):
        # Add rate limit headers if throttling information is available
        if hasattr(request, 'throttle_wait'):
            response['X-RateLimit-Limit'] = '100'
            response['X-RateLimit-Remaining'] = getattr(request, 'throttle_remaining', '0')
            response['X-RateLimit-Reset'] = str(int(time.time() + request.throttle_wait))
        
        return response
