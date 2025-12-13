"""
Management command to load production data from backup
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Load production data from backup file'

    def handle(self, *args, **options):
        backup_file = 'backend/data_backup.json'
        
        if not os.path.exists(backup_file):
            self.stdout.write(self.style.ERROR(f'Backup file not found: {backup_file}'))
            return
        
        self.stdout.write(self.style.SUCCESS('Loading data from backup...'))
        
        try:
            call_command('loaddata', backup_file, verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {str(e)}'))
