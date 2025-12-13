"""
QuerySet mixins for role-based filtering.
"""
from django.db.models import Q
from apps.authentication.models import Role
import logging

logger = logging.getLogger(__name__)


class RoleBasedQuerySetMixin:
    """
    Mixin to automatically filter querysets based on user role.
    
    This mixin should be used in ViewSets to ensure that users only see
    data they have permission to access based on their role.
    
    Usage:
        class MyViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
            queryset = MyModel.objects.all()
            serializer_class = MySerializer
    """
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        
        - ADMIN: See all records
        - SUPERVISOR: See records for their team (implementation depends on model)
        - OPERADOR: See only their own records
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return queryset.none()
        
        # Admins see everything
        if user.role.name == Role.ADMIN:
            return queryset
        
        # Apply role-based filtering
        return self.filter_by_role(queryset, user)
    
    def filter_by_role(self, queryset, user):
        """
        Apply role-based filtering to queryset.
        
        This method should be overridden in subclasses to implement
        specific filtering logic for each model.
        
        Args:
            queryset: The base queryset to filter
            user: The current user
            
        Returns:
            Filtered queryset based on user role
        """
        # Default implementation: filter by assigned_to or created_by
        if user.role.name == Role.SUPERVISOR:
            # Supervisors see their team's records
            # This is a simplified implementation - in production you'd have
            # a proper team/department structure
            return queryset
        
        elif user.role.name == Role.OPERADOR:
            # Operators only see their own records
            return self._filter_by_ownership(queryset, user)
        
        return queryset
    
    def _filter_by_ownership(self, queryset, user):
        """
        Filter queryset to only include records owned by the user.
        
        Checks common ownership fields: assigned_to, user, created_by, owner
        """
        model = queryset.model
        ownership_fields = []
        
        # Check which ownership fields exist in the model
        if hasattr(model, 'assigned_to'):
            ownership_fields.append('assigned_to')
        if hasattr(model, 'user'):
            ownership_fields.append('user')
        if hasattr(model, 'created_by'):
            ownership_fields.append('created_by')
        if hasattr(model, 'owner'):
            ownership_fields.append('owner')
        
        if not ownership_fields:
            logger.warning(
                f"Model {model.__name__} has no ownership fields. "
                f"Cannot filter by ownership for user {user.username}"
            )
            return queryset.none()
        
        # Build Q object for OR filtering across ownership fields
        q_objects = Q()
        for field in ownership_fields:
            q_objects |= Q(**{field: user})
        
        return queryset.filter(q_objects)


class OwnerFilterMixin:
    """
    Mixin to filter querysets by owner/assigned user.
    
    This is a simpler mixin that only filters by ownership,
    without considering supervisor access.
    
    Usage:
        class MyViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = MyModel.objects.all()
            serializer_class = MySerializer
            ownership_field = 'assigned_to'  # Specify the ownership field
    """
    
    ownership_field = 'assigned_to'  # Default ownership field
    
    def get_queryset(self):
        """Filter queryset to only show records owned by the user."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return queryset.none()
        
        # Admins see everything
        if user.role.name == Role.ADMIN:
            return queryset
        
        # Supervisors see everything (can be customized per ViewSet)
        if user.role.name == Role.SUPERVISOR:
            return queryset
        
        # Operators only see their own records
        return self.filter_by_owner(queryset, user)
    
    def filter_by_owner(self, queryset, user):
        """
        Filter queryset by ownership field.
        
        Args:
            queryset: The base queryset to filter
            user: The current user
            
        Returns:
            Filtered queryset containing only user's records
        """
        model = queryset.model
        
        # Check if ownership field exists
        if not hasattr(model, self.ownership_field):
            logger.error(
                f"Model {model.__name__} does not have field '{self.ownership_field}'. "
                f"Cannot filter by owner for user {user.username}"
            )
            return queryset.none()
        
        filter_kwargs = {self.ownership_field: user}
        return queryset.filter(**filter_kwargs)


class TeamFilterMixin:
    """
    Mixin to filter querysets by team for supervisors.
    
    This mixin allows supervisors to see records for their entire team,
    while operators only see their own records.
    
    Usage:
        class MyViewSet(TeamFilterMixin, viewsets.ModelViewSet):
            queryset = MyModel.objects.all()
            serializer_class = MySerializer
            team_field = 'assigned_to'  # Field that links to team members
    """
    
    team_field = 'assigned_to'  # Field that links to team members
    
    def get_queryset(self):
        """Filter queryset based on team membership."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return queryset.none()
        
        # Admins see everything
        if user.role.name == Role.ADMIN:
            return queryset
        
        # Supervisors see their team
        if user.role.name == Role.SUPERVISOR:
            return self.filter_by_team(queryset, user)
        
        # Operators only see their own records
        if user.role.name == Role.OPERADOR:
            return self.filter_by_owner(queryset, user)
        
        return queryset
    
    def filter_by_team(self, queryset, supervisor):
        """
        Filter queryset to show records for supervisor's team.
        
        In a simple implementation, this returns all records.
        In production, you would filter by department, area, or team structure.
        
        Args:
            queryset: The base queryset to filter
            supervisor: The supervisor user
            
        Returns:
            Filtered queryset for the team
        """
        # TODO: Implement proper team filtering based on your organization structure
        # For now, supervisors see everything (except what admins restrict)
        return queryset
    
    def filter_by_owner(self, queryset, user):
        """Filter queryset to only show records owned by the user."""
        model = queryset.model
        
        if not hasattr(model, self.team_field):
            logger.error(
                f"Model {model.__name__} does not have field '{self.team_field}'. "
                f"Cannot filter by owner for user {user.username}"
            )
            return queryset.none()
        
        filter_kwargs = {self.team_field: user}
        return queryset.filter(**filter_kwargs)


class AssetAccessMixin:
    """
    Mixin to filter querysets based on asset access.
    
    This mixin is used for models that are related to assets (like predictions).
    Users can only see records for assets they have access to.
    
    Usage:
        class PredictionViewSet(AssetAccessMixin, viewsets.ModelViewSet):
            queryset = Prediction.objects.all()
            serializer_class = PredictionSerializer
            asset_field = 'asset'  # Field that links to Asset model
    """
    
    asset_field = 'asset'  # Field that links to Asset model
    
    def get_queryset(self):
        """Filter queryset based on asset access."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user or not user.is_authenticated:
            return queryset.none()
        
        # Admins see everything
        if user.role.name == Role.ADMIN:
            return queryset
        
        # Filter by accessible assets
        return self.filter_by_asset_access(queryset, user)
    
    def filter_by_asset_access(self, queryset, user):
        """
        Filter queryset to only include records for accessible assets.
        
        An asset is accessible if:
        - User has a work order assigned for that asset (operators)
        - User is a supervisor (sees all assets in their area)
        
        Args:
            queryset: The base queryset to filter
            user: The current user
            
        Returns:
            Filtered queryset based on asset access
        """
        from apps.work_orders.models import WorkOrder
        
        model = queryset.model
        
        if not hasattr(model, self.asset_field):
            logger.error(
                f"Model {model.__name__} does not have field '{self.asset_field}'. "
                f"Cannot filter by asset access for user {user.username}"
            )
            return queryset.none()
        
        if user.role.name == Role.SUPERVISOR:
            # Supervisors see all assets (can be customized by area/department)
            return queryset
        
        elif user.role.name == Role.OPERADOR:
            # Operators only see assets from their assigned work orders
            accessible_assets = WorkOrder.objects.filter(
                assigned_to=user
            ).values_list('asset_id', flat=True).distinct()
            
            filter_kwargs = {f'{self.asset_field}__id__in': accessible_assets}
            return queryset.filter(**filter_kwargs)
        
        return queryset
