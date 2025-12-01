"""
URL configuration for CMMS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.core.views_admin import load_backup_data, seed_database

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Admin utilities (temporary - remove after use)
    path('api/admin/load-data/', load_backup_data, name='load-backup-data'),
    path('api/admin/seed-data/', seed_database, name='seed-database'),
    path('api/v1/admin/', include('apps.core.data_loader_urls')),
    
    # API v1
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/assets/', include('apps.assets.urls')),
    path('api/v1/work-orders/', include('apps.work_orders.urls')),
    path('api/v1/maintenance/', include('apps.maintenance.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/checklists/', include('apps.checklists.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/machine-status/', include('apps.machine_status.urls')),
    path('api/v1/configuration/', include('apps.configuration.urls')),
    path('api/v1/ml-predictions/', include('apps.ml_predictions.urls')),
    path('api/v1/bot/', include('apps.omnichannel_bot.urls')),
    path('api/v1/celery/', include('apps.core.celery_urls')),
    path('api/v1/dashboard/', include('apps.core.dashboard_urls')),
    path('api/v1/search/', include('apps.core.search_urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
