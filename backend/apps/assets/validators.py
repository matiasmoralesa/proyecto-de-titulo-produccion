"""
Validators for asset file uploads.
"""
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_file_size(file):
    """Validate file size (max 10MB)."""
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb}MB')


def validate_document_file(file):
    """Validate document file type and size."""
    # Allowed extensions
    allowed_extensions = [
        'pdf', 'doc', 'docx', 'xls', 'xlsx',
        'jpg', 'jpeg', 'png', 'gif',
        'txt', 'csv'
    ]
    
    # Validate extension
    validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
    validator(file)
    
    # Validate size
    validate_file_size(file)


def validate_image_file(file):
    """Validate image file type and size."""
    # Allowed extensions
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    
    # Validate extension
    validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
    validator(file)
    
    # Validate size (max 5MB for images)
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Image size cannot exceed {max_size_mb}MB')
