"""
Authentication models - User and Role.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class Role(models.Model):
    """Role model for RBAC."""
    ADMIN = 'ADMIN'
    SUPERVISOR = 'SUPERVISOR'
    OPERADOR = 'OPERADOR'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (SUPERVISOR, 'Supervisor'),
        (OPERADOR, 'Operador'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.get_name_display()


class UserManager(BaseUserManager):
    """Custom user manager."""
    
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('must_change_password', False)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Get or create ADMIN role
        from apps.authentication.models import Role
        admin_role, _ = Role.objects.get_or_create(
            name=Role.ADMIN,
            defaults={'description': 'Administrador del sistema'}
        )
        extra_fields.setdefault('role', admin_role)
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    phone = models.CharField(max_length=20, blank=True)
    must_change_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.role.name})"
    
    def has_role(self, role_name):
        """Check if user has a specific role."""
        return self.role.name == role_name
    
    def is_admin(self):
        """Check if user is admin."""
        return self.has_role(Role.ADMIN)
    
    def is_supervisor(self):
        """Check if user is supervisor."""
        return self.has_role(Role.SUPERVISOR)
    
    def is_operador(self):
        """Check if user is operador."""
        return self.has_role(Role.OPERADOR)
