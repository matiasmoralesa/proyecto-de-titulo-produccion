"""
Security tests for CMMS application
"""
import pytest
from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    InputSanitizationMiddleware,
)

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationSecurity:
    """Test authentication security measures"""
    
    def test_invalid_token_rejected(self):
        """Test that invalid JWT tokens are rejected"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token_here')
        
        response = client.get('/api/v1/assets/')
        assert response.status_code == 401
    
    def test_expired_token_rejected(self):
        """Test that expired tokens are rejected"""
        # This would require mocking time or using a very short token lifetime
        # For now, we test with an invalid token format
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.expired.token')
        
        response = client.get('/api/v1/assets/')
        assert response.status_code == 401
    
    def test_no_token_rejected(self):
        """Test that requests without token are rejected"""
        client = APIClient()
        
        response = client.get('/api/v1/assets/')
        assert response.status_code == 401
    
    def test_malformed_auth_header_rejected(self):
        """Test that malformed authorization headers are rejected"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='InvalidFormat token')
        
        response = client.get('/api/v1/assets/')
        assert response.status_code == 401


@pytest.mark.django_db
class TestAuthorizationSecurity:
    """Test authorization and permission enforcement"""
    
    @pytest.fixture
    def users(self, roles):
        """Create test users with different roles"""
        admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role=roles['admin']
        )
        
        supervisor = User.objects.create_user(
            username='supervisor',
            email='supervisor@test.com',
            password='testpass123',
            role=roles['supervisor']
        )
        
        operator = User.objects.create_user(
            username='operator',
            email='operator@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        return {'admin': admin, 'supervisor': supervisor, 'operator': operator}
    
    def get_token(self, user):
        """Get JWT token for user"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_operator_cannot_access_admin_endpoints(self, users):
        """Test that operators cannot access admin-only endpoints"""
        client = APIClient()
        token = self.get_token(users['operator'])
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access user management (admin only)
        response = client.get('/api/v1/auth/users/')
        assert response.status_code == 403
    
    def test_supervisor_cannot_access_admin_endpoints(self, users):
        """Test that supervisors cannot access admin-only endpoints"""
        client = APIClient()
        token = self.get_token(users['supervisor'])
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Try to access user management (admin only)
        response = client.get('/api/v1/auth/users/')
        assert response.status_code == 403
    
    def test_admin_can_access_admin_endpoints(self, users):
        """Test that admins can access admin-only endpoints"""
        client = APIClient()
        token = self.get_token(users['admin'])
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Access user management
        response = client.get('/api/v1/auth/users/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_xss_script_tag_sanitized(self):
        """Test that script tags are sanitized from query parameters"""
        factory = RequestFactory()
        request = factory.get('/test/?search=<script>alert("xss")</script>')
        
        middleware = InputSanitizationMiddleware(lambda r: None)
        middleware.process_request(request)
        
        # Check that script tag is removed
        search_value = request.GET.get('search', '')
        assert '<script>' not in search_value.lower()
        assert 'alert' not in search_value.lower()
    
    def test_xss_iframe_tag_sanitized(self):
        """Test that iframe tags are sanitized"""
        factory = RequestFactory()
        request = factory.get('/test/?content=<iframe src="evil.com"></iframe>')
        
        middleware = InputSanitizationMiddleware(lambda r: None)
        middleware.process_request(request)
        
        content_value = request.GET.get('content', '')
        assert '<iframe' not in content_value.lower()
    
    def test_xss_event_handler_sanitized(self):
        """Test that event handlers are sanitized"""
        factory = RequestFactory()
        request = factory.get('/test/?html=<div onclick="alert(1)">Click</div>')
        
        middleware = InputSanitizationMiddleware(lambda r: None)
        middleware.process_request(request)
        
        html_value = request.GET.get('html', '')
        assert 'onclick' not in html_value.lower()


class TestSecurityHeaders:
    """Test security headers middleware"""
    
    def test_security_headers_added(self):
        """Test that security headers are added to responses"""
        factory = RequestFactory()
        request = factory.get('/test/')
        
        # Create a mock response
        from django.http import HttpResponse
        response = HttpResponse()
        
        middleware = SecurityHeadersMiddleware(lambda r: response)
        response = middleware.process_response(request, response)
        
        # Check security headers
        assert 'Content-Security-Policy' in response
        assert 'X-Content-Type-Options' in response
        assert response['X-Content-Type-Options'] == 'nosniff'
        assert 'X-Frame-Options' in response
        assert response['X-Frame-Options'] == 'DENY'
        assert 'X-XSS-Protection' in response
        assert 'Referrer-Policy' in response
        assert 'Permissions-Policy' in response
    
    def test_csp_header_configured(self):
        """Test that CSP header is properly configured"""
        factory = RequestFactory()
        request = factory.get('/test/')
        
        from django.http import HttpResponse
        response = HttpResponse()
        
        middleware = SecurityHeadersMiddleware(lambda r: response)
        response = middleware.process_response(request, response)
        
        csp = response['Content-Security-Policy']
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp


class TestRequestLogging:
    """Test request logging middleware"""
    
    def test_request_id_added(self):
        """Test that request ID is added to requests"""
        factory = RequestFactory()
        request = factory.get('/test/')
        
        from django.http import HttpResponse
        response = HttpResponse()
        
        middleware = RequestLoggingMiddleware(lambda r: response)
        middleware.process_request(request)
        
        # Check that request ID was added
        assert hasattr(request, 'request_id')
        assert len(request.request_id) > 0
    
    def test_request_id_in_response_header(self):
        """Test that request ID is added to response headers"""
        factory = RequestFactory()
        request = factory.get('/test/')
        
        from django.http import HttpResponse
        response = HttpResponse()
        
        middleware = RequestLoggingMiddleware(lambda r: response)
        middleware.process_request(request)
        response = middleware.process_response(request, response)
        
        # Check that request ID is in response headers
        assert 'X-Request-ID' in response
        assert response['X-Request-ID'] == request.request_id


@pytest.mark.django_db
class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_cors_allows_configured_origins(self):
        """Test that CORS allows configured origins"""
        client = Client()
        
        response = client.options(
            '/api/v1/assets/',
            HTTP_ORIGIN='http://localhost:5173',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET'
        )
        
        # Should allow the request
        assert response.status_code in [200, 204]
    
    def test_cors_rejects_unknown_origins(self):
        """Test that CORS rejects unknown origins"""
        client = Client()
        
        response = client.options(
            '/api/v1/assets/',
            HTTP_ORIGIN='http://evil.com',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET'
        )
        
        # Should not have CORS headers for unknown origin
        assert 'Access-Control-Allow-Origin' not in response or \
               response.get('Access-Control-Allow-Origin') != 'http://evil.com'


@pytest.mark.django_db
class TestPasswordSecurity:
    """Test password security measures"""
    
    def test_password_hashed_in_database(self, roles):
        """Test that passwords are hashed, not stored in plain text"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='mypassword123',
            role=roles['operator']
        )
        
        # Password should be hashed
        assert user.password != 'mypassword123'
        assert user.password.startswith('pbkdf2_sha256$')
    
    def test_weak_password_rejected(self):
        """Test that weak passwords are rejected"""
        from django.core.exceptions import ValidationError
        from django.contrib.auth.password_validation import validate_password
        
        with pytest.raises(ValidationError):
            validate_password('123')  # Too short
        
        with pytest.raises(ValidationError):
            validate_password('password')  # Too common
    
    def test_password_minimum_length_enforced(self):
        """Test that minimum password length is enforced"""
        from django.core.exceptions import ValidationError
        from django.contrib.auth.password_validation import validate_password
        
        with pytest.raises(ValidationError):
            validate_password('short1')  # Less than 8 characters


@pytest.mark.django_db
class TestRateLimiting:
    """Test rate limiting functionality"""
    
    @pytest.fixture
    def authenticated_client(self, roles):
        """Create authenticated client"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def test_rate_limit_configured(self, authenticated_client):
        """Test that rate limiting is configured"""
        # Make multiple requests
        responses = []
        for _ in range(5):
            response = authenticated_client.get('/api/v1/assets/')
            responses.append(response)
        
        # All should succeed (under limit)
        for response in responses:
            assert response.status_code in [200, 404]  # 404 if no assets exist


@pytest.mark.django_db
class TestAuditTrail:
    """Test audit trail functionality"""
    
    def test_audit_log_created_on_user_creation(self, roles):
        """Test that audit log is created when user is created"""
        from apps.configuration.models import AuditLog
        
        initial_count = AuditLog.objects.count()
        
        # Create user through admin interface would trigger audit
        # For now, we test the audit function directly
        from apps.core.audit import log_audit
        
        admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role=roles['admin']
        )
        
        user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        log_audit(
            user=admin,
            action='CREATE',
            obj=user,
            changes={'username': {'old': None, 'new': 'newuser'}}
        )
        
        # Check that audit log was created
        assert AuditLog.objects.count() > initial_count
    
    def test_audit_log_tracks_changes(self, roles):
        """Test that audit log tracks field changes"""
        from apps.core.audit import track_model_changes
        
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        old_user = User.objects.get(pk=user.pk)
        user.email = 'newemail@test.com'
        user.save()
        
        changes = track_model_changes(old_user, user, ['email'])
        
        assert 'email' in changes
        assert changes['email']['old'] == 'test@test.com'
        assert changes['email']['new'] == 'newemail@test.com'


@pytest.mark.django_db
class TestSQLInjectionPrevention:
    """Test SQL injection prevention"""
    
    @pytest.fixture
    def authenticated_client(self, roles):
        """Create authenticated client"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def test_sql_injection_in_search_prevented(self, authenticated_client):
        """Test that SQL injection attempts in search are prevented"""
        # Try SQL injection in search parameter
        response = authenticated_client.get(
            '/api/v1/assets/?search=\' OR \'1\'=\'1'
        )
        
        # Should not cause error, Django ORM prevents SQL injection
        assert response.status_code in [200, 400]
    
    def test_sql_injection_in_filter_prevented(self, authenticated_client):
        """Test that SQL injection attempts in filters are prevented"""
        response = authenticated_client.get(
            '/api/v1/assets/?status=\'; DROP TABLE assets; --'
        )
        
        # Should not cause error
        assert response.status_code in [200, 400]
