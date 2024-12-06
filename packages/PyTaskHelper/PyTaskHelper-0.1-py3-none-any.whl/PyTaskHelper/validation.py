import re

def is_valid_email(email):
    """Validate an email address."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_phone(phone):
    """Validate a phone number."""
    regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
    return re.match(regex, phone) is not None
