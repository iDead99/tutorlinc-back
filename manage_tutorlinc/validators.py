from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_file_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_file_size:
        raise ValidationError(f"File size should not exceed 5 MB.")
