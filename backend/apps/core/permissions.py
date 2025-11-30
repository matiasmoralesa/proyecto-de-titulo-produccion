"""
Shared permission classes.
Re-export from authentication app for convenience.
"""
from apps.authentication.permissions import (
    IsAdmin,
    IsSupervisorOrAdmin,
    IsOperadorOrAbove,
    IsOwnerOrSupervisor,
)

__all__ = [
    'IsAdmin',
    'IsSupervisorOrAdmin',
    'IsOperadorOrAbove',
    'IsOwnerOrSupervisor',
]
