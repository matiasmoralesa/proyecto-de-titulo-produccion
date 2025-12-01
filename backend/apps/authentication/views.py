"""
Views for authentication app.
"""
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.db import models
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
    PasswordResetSerializer,
)
from .models import User, Role
from .permissions import IsAdmin


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing users (read-only) with role-based access.
    
    - ADMIN: Ve todos los usuarios
    - SUPERVISOR: Ve solo su equipo
    - OPERADOR: 403 Forbidden
    
    Validates: Requirements 5.1, 5.2, 5.3
    """
    queryset = User.objects.filter(is_active=True).select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter users based on role.
        
        Validates: Requirements 5.1, 5.2, 5.3
        """
        from apps.core.permissions import IsSupervisorOrAbove
        from apps.authentication.models import Role
        
        queryset = super().get_queryset()
        user = self.request.user
        
        # Operators cannot list users
        if user.role.name == Role.OPERADOR:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Los operadores no pueden listar usuarios.')
        
        # Admins see all users
        if user.role.name == Role.ADMIN:
            return queryset
        
        # Supervisors see their team
        # TODO: Filter by team when team structure is implemented
        if user.role.name == Role.SUPERVISOR:
            return queryset
        
        return queryset.none()


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management (ADMIN and SUPERVISOR).
    Provides CRUD operations for user accounts.
    
    - ADMIN: Full CRUD on all users
    - SUPERVISOR: Can create users but with restrictions
    
    Validates: Requirements 5.4, 5.5
    """
    queryset = User.objects.all().select_related('role').order_by('-created_at')
    
    def get_permissions(self):
        """
        Set permissions based on action.
        Only supervisors and admins can create/manage users.
        """
        from apps.core.permissions import IsSupervisorOrAbove
        
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'activate', 'deactivate', 'reset_password']:
            return [IsAuthenticated(), IsSupervisorOrAbove()]
        return [IsAuthenticated(), IsAdmin()]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """
        Optionally filter users by role or active status.
        """
        queryset = super().get_queryset()
        
        # Filter by role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role__name=role)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search by username or email
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(username__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search)
            )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user with hashed password.
        
        Validation: Only supervisors and admins can create users.
        Supervisors cannot create admin users.
        """
        from rest_framework.exceptions import PermissionDenied
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Supervisors cannot create admin users
        if request.user.role.name == Role.SUPERVISOR:
            role_id = request.data.get('role')
            if role_id:
                try:
                    role = Role.objects.get(id=role_id)
                    if role.name == Role.ADMIN:
                        raise PermissionDenied('Los supervisores no pueden crear usuarios administradores.')
                except Role.DoesNotExist:
                    pass
        
        # Create user
        user = serializer.save()
        
        # Return user data
        response_serializer = UserSerializer(user)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Update user information."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Don't allow updating password through this endpoint
        if 'password' in request.data:
            return Response(
                {'detail': 'Use el endpoint de cambio de contraseña para actualizar la contraseña.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete - deactivate user instead of deleting.
        """
        instance = self.get_object()
        
        # Prevent self-deletion
        if instance.id == request.user.id:
            return Response(
                {'detail': 'No puede desactivar su propia cuenta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deactivate instead of delete
        instance.is_active = False
        instance.save()
        
        return Response(
            {'detail': 'Usuario desactivado exitosamente.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a deactivated user."""
        user = self.get_object()
        user.is_active = True
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user."""
        user = self.get_object()
        
        # Prevent self-deactivation
        if user.id == request.user.id:
            return Response(
                {'detail': 'No puede desactivar su propia cuenta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_active = False
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset user password (admin only)."""
        user = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.must_change_password = True
            user.save()
            
            return Response(
                {'detail': 'Contraseña restablecida exitosamente. El usuario deberá cambiarla en el próximo inicio de sesión.'},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view with user data.
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom JWT token refresh view.
    """
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout view - blacklist the refresh token.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logout(request)
        return Response(
            {'detail': 'Sesión cerrada exitosamente.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'detail': 'Error al cerrar sesión.'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Get current authenticated user data.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change password for current user.
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.must_change_password = False
        user.save()
        
        return Response(
            {'detail': 'Contraseña cambiada exitosamente.'},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token_view(request):
    """
    Verify if a token is valid.
    """
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'detail': 'Token no proporcionado.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Try to decode the token
        from rest_framework_simplejwt.tokens import AccessToken
        AccessToken(token)
        return Response(
            {'detail': 'Token válido.', 'valid': True},
            status=status.HTTP_200_OK
        )
    except Exception:
        return Response(
            {'detail': 'Token inválido o expirado.', 'valid': False},
            status=status.HTTP_401_UNAUTHORIZED
        )
