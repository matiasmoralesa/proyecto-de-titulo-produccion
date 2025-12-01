"""
Middleware for auditing access to resources.

Validates: Requirements 9.1, 9.2, 9.3, 9.4
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from apps.configuration.models import AccessLog

logger = logging.getLogger(__name__)


class AccessAuditMiddleware(MiddlewareMixin):
    """
    Middleware to log all access attempts to resources.
    
    Logs successful and failed access attempts for security auditing.
    Validates: Requirements 9.1, 9.2, 9.3
    """
    
    # Paths to audit
    AUDIT_PATHS = [
        '/api/v1/work-orders/',
        '/api/v1/assets/',
        '/api/v1/predictions/',
        '/api/v1/reports/',
        '/api/v1/auth/users/',
        '/api/v1/configuration/',
    ]
    
    # Actions that should be audited
    AUDIT_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    
    def process_response(self, request, response):
        """
        Log access after response is generated.
        
        Validates: Requirements 9.1, 9.2
        """
        # Only audit API requests
        if not request.path.startswith('/api/'):
            return response
        
        # Check if path should be audited
        should_audit = any(
            request.path.startswith(path) 
            for path in self.AUDIT_PATHS
        )
        
        if not should_audit:
            return response
        
        # Only audit specific methods
        if request.method not in self.AUDIT_METHODS:
            return response
        
        # Extract information
        user = request.user if request.user.is_authenticated else None
        resource_type = self._extract_resource_type(request.path)
        resource_id = self._extract_resource_id(request.path)
        action = self._map_method_to_action(request.method)
        success = 200 <= response.status_code < 400
        ip_address = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        # Additional details
        details = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
        }
        
        # Log failed access attempts with more details
        if not success:
            details['reason'] = self._get_failure_reason(response.status_code)
            logger.warning(
                f"Access denied: {user.username if user else 'Anonymous'} "
                f"tried to {action} {resource_type} {resource_id} - "
                f"Status: {response.status_code}"
            )
        
        # Create access log entry
        try:
            AccessLog.objects.create(
                user=user,
                resource_type=resource_type,
                resource_id=resource_id or 'list',
                action=action,
                success=success,
                ip_address=ip_address,
                user_agent=user_agent,
                details=details
            )
        except Exception as e:
            # Don't fail the request if logging fails
            logger.error(f"Failed to create access log: {e}")
        
        return response
    
    def _extract_resource_type(self, path):
        """Extract resource type from path."""
        parts = path.strip('/').split('/')
        if len(parts) >= 3:
            return parts[2]  # e.g., /api/v1/work-orders/ -> work-orders
        return 'unknown'
    
    def _extract_resource_id(self, path):
        """Extract resource ID from path if present."""
        parts = path.strip('/').split('/')
        if len(parts) >= 4 and parts[3]:
            # Check if it's a UUID or number
            resource_id = parts[3]
            if resource_id and not resource_id.isalpha():
                return resource_id
        return None
    
    def _map_method_to_action(self, method):
        """Map HTTP method to action."""
        mapping = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }
        return mapping.get(method, method.lower())
    
    def _get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_failure_reason(self, status_code):
        """Get human-readable failure reason."""
        reasons = {
            401: 'Unauthorized - Authentication required',
            403: 'Forbidden - Insufficient permissions',
            404: 'Not Found - Resource does not exist or access denied',
            400: 'Bad Request - Invalid data',
            500: 'Server Error',
        }
        return reasons.get(status_code, f'HTTP {status_code}')


class SecurityAlertMiddleware(MiddlewareMixin):
    """
    Middleware to detect and alert on suspicious activity.
    
    Validates: Requirements 9.4
    """
    
    # Threshold for failed attempts before alerting
    FAILED_ATTEMPTS_THRESHOLD = 5
    TIME_WINDOW_MINUTES = 5
    
    def process_response(self, request, response):
        """
        Check for suspicious activity patterns.
        
        Validates: Requirements 9.4
        """
        # Only check for failed access attempts
        if response.status_code not in [401, 403]:
            return response
        
        user = request.user if request.user.is_authenticated else None
        
        if user:
            # Check recent failed attempts
            from django.utils import timezone
            from datetime import timedelta
            
            time_threshold = timezone.now() - timedelta(minutes=self.TIME_WINDOW_MINUTES)
            
            recent_failures = AccessLog.objects.filter(
                user=user,
                success=False,
                timestamp__gte=time_threshold
            ).count()
            
            if recent_failures >= self.FAILED_ATTEMPTS_THRESHOLD:
                logger.critical(
                    f"SECURITY ALERT: User {user.username} has {recent_failures} "
                    f"failed access attempts in the last {self.TIME_WINDOW_MINUTES} minutes"
                )
                
                # TODO: Send notification to admins
                # TODO: Consider temporary account lockout
        
        return response
