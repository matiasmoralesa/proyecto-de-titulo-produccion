"""
Middleware for authentication logging and security.
"""
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AuthenticationLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log authentication attempts and failures.
    """
    
    def process_request(self, request):
        """Log authentication attempts."""
        # Log login attempts
        if request.path.endswith('/auth/login/') and request.method == 'POST':
            try:
                username = request.POST.get('username', 'unknown')
                logger.info(f'Login attempt for user: {username} from IP: {self.get_client_ip(request)}')
            except Exception:
                pass
        
        return None
    
    def process_response(self, request, response):
        """Log authentication failures."""
        # Log failed login attempts
        if request.path.endswith('/auth/login/') and request.method == 'POST':
            try:
                if response.status_code == 401:
                    username = request.POST.get('username', 'unknown')
                    logger.warning(
                        f'Failed login attempt for user: {username} from IP: {self.get_client_ip(request)}'
                    )
                elif response.status_code == 200:
                    username = request.POST.get('username', 'unknown')
                    logger.info(f'Successful login for user: {username}')
            except Exception:
                pass
        
        # Log unauthorized access attempts
        if response.status_code == 403:
            try:
                user = getattr(request, 'user', None)
                username = user.username if user and user.is_authenticated else 'anonymous'
                logger.warning(
                    f'Unauthorized access attempt by user: {username} to path: {request.path}'
                )
            except Exception:
                pass
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
