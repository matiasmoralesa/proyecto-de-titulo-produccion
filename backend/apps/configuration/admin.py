from django.contrib import admin
from apps.configuration.models import (
    AssetCategory,
    Priority,
    WorkOrderType,
    SystemParameter,
    AuditLog
)


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['name']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'color_code', 'is_active', 'created_at']
    list_filter = ['is_active', 'level']
    search_fields = ['name', 'description']
    ordering = ['level']


@admin.register(WorkOrderType)
class WorkOrderTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'requires_approval', 'is_active', 'created_at']
    list_filter = ['is_active', 'requires_approval', 'created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['name']


@admin.register(SystemParameter)
class SystemParameterAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'data_type', 'is_editable', 'updated_at']
    list_filter = ['data_type', 'is_editable']
    search_fields = ['key', 'description']
    ordering = ['key']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'model_name', 'object_repr']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['object_repr', 'user__username']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp', 'user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
