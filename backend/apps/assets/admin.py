"""
Admin configuration for assets app.
"""
from django.contrib import admin
from .models import Location, Asset  # AssetDocument comentado


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin for Location model."""
    list_display = ['name', 'address', 'created_at']
    search_fields = ['name', 'address', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'coordinates', 'description')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# AssetDocumentInline comentado - funcionalidad de documentos removida
# class AssetDocumentInline(admin.TabularInline):
#     """Inline admin for asset documents."""
#     model = AssetDocument
#     extra = 0
#     readonly_fields = ['created_at', 'uploaded_by']
#     fields = ['title', 'document_type', 'file', 'description', 'uploaded_by', 'created_at']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin for Asset model."""
    list_display = [
        'name', 'vehicle_type', 'serial_number', 'license_plate',
        'status', 'location', 'is_archived', 'created_at'
    ]
    list_filter = ['vehicle_type', 'status', 'is_archived', 'location']
    search_fields = ['name', 'serial_number', 'license_plate', 'model']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    # inlines = [AssetDocumentInline]  # Comentado - funcionalidad removida
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'vehicle_type', 'model')
        }),
        ('Identification', {
            'fields': ('serial_number', 'license_plate')
        }),
        ('Location & Status', {
            'fields': ('location', 'installation_date', 'status', 'is_archived')
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# AssetDocumentAdmin comentado - funcionalidad de documentos removida
# @admin.register(AssetDocument)
# class AssetDocumentAdmin(admin.ModelAdmin):
#     """Admin for AssetDocument model."""
#     list_display = ['title', 'asset', 'document_type', 'uploaded_by', 'created_at']
#     list_filter = ['document_type', 'created_at']
#     search_fields = ['title', 'description', 'asset__name']
#     readonly_fields = ['id', 'created_at', 'updated_at', 'uploaded_by']
#     
#     fieldsets = (
#         (None, {
#             'fields': ('asset', 'title', 'document_type', 'file', 'description')
#         }),
#         ('Metadata', {
#             'fields': ('id', 'uploaded_by', 'created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     
#     def save_model(self, request, obj, form, change):
#         """Set uploaded_by on creation."""
#         if not change:
#             obj.uploaded_by = request.user
#         super().save_model(request, obj, form, change)
