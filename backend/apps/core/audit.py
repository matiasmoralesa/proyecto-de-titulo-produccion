"""
Audit trail system for tracking configuration and user management changes
"""
import logging
from apps.configuration.models import AuditLog

logger = logging.getLogger(__name__)


def log_audit(user, action, obj=None, changes=None, request=None):
    """
    Helper function to create audit log entries
    
    Args:
        user: User performing the action
        action: Action being performed (use AuditLog.ACTION_* constants)
        obj: Object being modified (optional)
        changes: Dictionary of changes (optional)
        request: HTTP request object (optional)
    """
    try:
        audit_data = {
            'user': user,
            'action': action,
            'changes': changes or {},
        }
        
        # Add object information if provided
        if obj:
            audit_data['content_object'] = obj
            audit_data['object_repr'] = str(obj)
        
        # Add request information if provided
        if request:
            audit_data['ip_address'] = get_client_ip(request)
            audit_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:500]
            audit_data['request_id'] = getattr(request, 'request_id', '')
        
        # Create audit log entry
        audit_log = AuditLog.objects.create(**audit_data)
        
        # Also log to file
        logger.info(
            f'Audit: {action}',
            extra={
                'audit_id': str(audit_log.id),
                'user': str(user),
                'action': action,
                'object': str(obj) if obj else None,
                'changes': changes or {},
            }
        )
        
        return audit_log
        
    except Exception as e:
        logger.error(f'Failed to create audit log: {e}', exc_info=True)
        return None


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_model_changes(old_instance, new_instance, fields_to_track=None):
    """
    Compare two model instances and return dictionary of changes
    
    Args:
        old_instance: Original model instance
        new_instance: Updated model instance
        fields_to_track: List of field names to track (None = all fields)
    
    Returns:
        Dictionary with 'old' and 'new' values for changed fields
    """
    changes = {}
    
    if not old_instance or not new_instance:
        return changes
    
    # Get fields to compare
    if fields_to_track is None:
        fields_to_track = [f.name for f in new_instance._meta.fields]
    
    for field_name in fields_to_track:
        try:
            old_value = getattr(old_instance, field_name, None)
            new_value = getattr(new_instance, field_name, None)
            
            # Skip if values are the same
            if old_value == new_value:
                continue
            
            # Convert to string for JSON serialization
            changes[field_name] = {
                'old': str(old_value) if old_value is not None else None,
                'new': str(new_value) if new_value is not None else None,
            }
        except Exception as e:
            logger.warning(f'Failed to track change for field {field_name}: {e}')
    
    return changes
