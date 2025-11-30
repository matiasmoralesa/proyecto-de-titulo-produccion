"""
Script to create media directories for file storage.
"""
import os
from pathlib import Path

# Get base directory
BASE_DIR = Path(__file__).resolve().parent

# Media directories to create
MEDIA_DIRS = [
    'media/assets/documents',
    'media/assets/photos',
    'media/checklists/pdfs',
    'media/checklists/photos',
]

def create_media_directories():
    """Create all media directories."""
    for dir_path in MEDIA_DIRS:
        full_path = BASE_DIR / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f'✓ Created directory: {dir_path}')
        
        # Create .gitkeep file
        gitkeep_path = full_path / '.gitkeep'
        gitkeep_path.touch(exist_ok=True)
    
    print('\n✓ All media directories created successfully!')

if __name__ == '__main__':
    create_media_directories()
