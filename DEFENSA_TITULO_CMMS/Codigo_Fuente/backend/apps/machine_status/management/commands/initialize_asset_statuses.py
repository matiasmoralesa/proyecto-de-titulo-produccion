"""
Django management command to initialize asset statuses for all assets.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.assets.models import Asset
from apps.machine_status.models import AssetStatus
from apps.authentication.models import User, Role


class Command(BaseCommand):
    help = 'Initialize asset statuses for all assets that do not have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if status already exists',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        
        self.stdout.write(self.style.SUCCESS('Starting asset status initialization...'))
        
        # Get an admin user to assign as the creator
        try:
            admin_user = User.objects.filter(role__name=Role.ADMIN, is_active=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR('No active admin user found. Please create an admin user first.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error finding admin user: {e}'))
            return
        
        # Get all active assets
        assets = Asset.objects.filter(is_archived=False)
        total_assets = assets.count()
        
        if total_assets == 0:
            self.stdout.write(self.style.WARNING('No active assets found.'))
            return
        
        self.stdout.write(f'Found {total_assets} active assets.')
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        with transaction.atomic():
            for asset in assets:
                try:
                    # Check if status already exists
                    status_exists = AssetStatus.objects.filter(asset=asset).exists()
                    
                    if status_exists and not force:
                        self.stdout.write(f'  - Skipping {asset.name} (status already exists)')
                        skipped_count += 1
                        continue
                    
                    if status_exists and force:
                        # Delete existing status
                        AssetStatus.objects.filter(asset=asset).delete()
                        self.stdout.write(f'  - Deleted existing status for {asset.name}')
                    
                    # Create initial status
                    AssetStatus.objects.create(
                        asset=asset,
                        status_type=AssetStatus.OPERANDO,
                        odometer_reading=0.0,
                        fuel_level=100,
                        condition_notes='Estado inicial - Sistema inicializado',
                        last_updated_by=admin_user
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created status for {asset.name}'))
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error creating status for {asset.name}: {e}'))
                    error_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Asset Status Initialization Complete!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Total assets: {total_assets}')
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))
        self.stdout.write('='*50)
