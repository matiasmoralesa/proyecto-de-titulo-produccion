#!/usr/bin/env python3
"""
Script para crear directorios de media necesarios
"""
import os
from pathlib import Path

def setup_media_directories():
    """Create necessary media directories."""
    base_dir = Path(__file__).resolve().parent
    media_root = base_dir / 'media'
    
    # Create media directories
    directories = [
        media_root / 'checklists' / 'pdfs',
        media_root / 'checklists' / 'photos',
        media_root / 'assets' / 'documents',
        media_root / 'work_orders' / 'attachments',
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
        
        # Create .gitkeep file to ensure directory exists in git
        gitkeep_file = directory / '.gitkeep'
        if not gitkeep_file.exists():
            gitkeep_file.touch()
            print(f"Created .gitkeep in: {directory}")

if __name__ == '__main__':
    setup_media_directories()