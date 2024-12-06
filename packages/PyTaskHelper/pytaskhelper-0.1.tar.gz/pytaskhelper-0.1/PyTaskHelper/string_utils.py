def snake_to_camel(snake_str):
    """Convert snake_case to CamelCase."""
    return ''.join(word.capitalize() for word in snake_str.split('_'))

def camel_to_snake(camel_str):
    """Convert CamelCase to snake_case."""
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
