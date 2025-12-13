"""
Query optimization utilities for CMMS application
"""
from django.db import connection
from django.db.models import Prefetch
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)


def log_queries(func):
    """
    Decorator to log database queries for a function
    Useful for development to identify N+1 queries
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Reset queries
        connection.queries_log.clear()
        
        # Execute function
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log results
        num_queries = len(connection.queries)
        execution_time = end_time - start_time
        
        logger.info(
            f'{func.__name__} executed {num_queries} queries in {execution_time:.2f}s'
        )
        
        if num_queries > 10:
            logger.warning(
                f'{func.__name__} executed {num_queries} queries - consider optimization'
            )
        
        return result
    
    return wrapper


class QueryOptimizer:
    """
    Utility class for common query optimizations
    """
    
    @staticmethod
    def optimize_asset_queryset(queryset):
        """
        Optimize Asset queryset with select_related and prefetch_related
        """
        return queryset.select_related(
            'location',
            'created_by'
        ).prefetch_related(
            'documents',
            'work_orders',
            'maintenance_plans'
        )
    
    @staticmethod
    def optimize_work_order_queryset(queryset):
        """
        Optimize WorkOrder queryset
        """
        return queryset.select_related(
            'asset',
            'asset__location',
            'assigned_to',
            'created_by'
        ).prefetch_related(
            'checklist_responses'
        )
    
    @staticmethod
    def optimize_maintenance_plan_queryset(queryset):
        """
        Optimize MaintenancePlan queryset
        """
        return queryset.select_related(
            'asset',
            'asset__location',
            'created_by'
        )
    
    @staticmethod
    def optimize_inventory_queryset(queryset):
        """
        Optimize SparePart queryset
        """
        return queryset.prefetch_related(
            'stock_movements',
            'usage_history'
        )
    
    @staticmethod
    def optimize_checklist_queryset(queryset):
        """
        Optimize ChecklistResponse queryset
        """
        return queryset.select_related(
            'template',
            'asset',
            'work_order',
            'completed_by'
        ).prefetch_related(
            'item_responses'
        )
    
    @staticmethod
    def optimize_notification_queryset(queryset):
        """
        Optimize Notification queryset
        """
        return queryset.select_related(
            'user'
        )
    
    @staticmethod
    def optimize_prediction_queryset(queryset):
        """
        Optimize FailurePrediction queryset
        """
        return queryset.select_related(
            'asset',
            'asset__location',
            'work_order_created'
        )


def add_database_indexes():
    """
    SQL commands to add recommended indexes
    Run this as a migration or management command
    """
    indexes = [
        # Assets
        "CREATE INDEX IF NOT EXISTS idx_assets_status ON assets_asset(status);",
        "CREATE INDEX IF NOT EXISTS idx_assets_vehicle_type ON assets_asset(vehicle_type);",
        "CREATE INDEX IF NOT EXISTS idx_assets_location ON assets_asset(location_id);",
        
        # Work Orders
        "CREATE INDEX IF NOT EXISTS idx_wo_status ON work_orders_workorder(status);",
        "CREATE INDEX IF NOT EXISTS idx_wo_priority ON work_orders_workorder(priority);",
        "CREATE INDEX IF NOT EXISTS idx_wo_asset ON work_orders_workorder(asset_id);",
        "CREATE INDEX IF NOT EXISTS idx_wo_assigned ON work_orders_workorder(assigned_to_id);",
        "CREATE INDEX IF NOT EXISTS idx_wo_scheduled ON work_orders_workorder(scheduled_date);",
        
        # Maintenance Plans
        "CREATE INDEX IF NOT EXISTS idx_mp_asset ON maintenance_maintenanceplan(asset_id);",
        "CREATE INDEX IF NOT EXISTS idx_mp_active ON maintenance_maintenanceplan(is_active);",
        "CREATE INDEX IF NOT EXISTS idx_mp_next_due ON maintenance_maintenanceplan(next_due_date);",
        
        # Inventory
        "CREATE INDEX IF NOT EXISTS idx_sp_quantity ON inventory_sparepart(quantity);",
        "CREATE INDEX IF NOT EXISTS idx_sp_min_qty ON inventory_sparepart(minimum_quantity);",
        
        # Notifications
        "CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications_notification(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_notif_read ON notifications_notification(is_read);",
        "CREATE INDEX IF NOT EXISTS idx_notif_created ON notifications_notification(created_at);",
        
        # Predictions
        "CREATE INDEX IF NOT EXISTS idx_pred_asset ON failure_predictions(asset_id);",
        "CREATE INDEX IF NOT EXISTS idx_pred_risk ON failure_predictions(risk_level);",
        "CREATE INDEX IF NOT EXISTS idx_pred_date ON failure_predictions(prediction_date);",
    ]
    
    return indexes
