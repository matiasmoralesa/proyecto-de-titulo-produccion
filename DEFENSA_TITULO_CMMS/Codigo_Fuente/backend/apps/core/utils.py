"""
Shared utility functions.
"""


def generate_unique_code(prefix, model_class, field_name='code'):
    """
    Generate a unique code with a given prefix.
    
    Args:
        prefix: String prefix for the code
        model_class: Django model class
        field_name: Field name to check for uniqueness
    
    Returns:
        Unique code string
    """
    import random
    import string
    
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=6))
        code = f"{prefix}-{random_suffix}"
        
        filter_kwargs = {field_name: code}
        if not model_class.objects.filter(**filter_kwargs).exists():
            return code
