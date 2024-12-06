import re

def is_valid_email(email):
    """Validate an email address."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_phone(phone):
    """Validate a phone number with stricter rules."""
    # The phone number must have 10-15 digits, possibly prefixed with a "+"
    regex = r'^\+?[1-9]\d{9,14}$'  # E.164 format, at least 10 digits
    return re.match(regex, phone) is not None
