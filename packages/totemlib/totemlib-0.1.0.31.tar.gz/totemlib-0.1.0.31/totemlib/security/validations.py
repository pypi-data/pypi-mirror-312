# Validaciones genéricas estándar
# Creado por: Totem Bear
# Fecha: 05-Sep-2023

from collections import deque
from datetime import datetime

def string_to_type(type_str):
    types_map = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'datetime': datetime
    }
    
    if type_str not in types_map:
        raise ValueError(f"TotemLib-Security - string_to_type-ERROR: Invalid data type {type_str}.")
    
    return types_map[type_str]


def string_to_datetime(date_str: str, date_format: str) -> datetime:
    try:
        return datetime.strptime(date_str, date_format)
    except Exception as e:
        raise ValueError(f"TotemLib-Security - string_to_datetime-ERROR: "\
                         f"Invalid data type {date_str}.")
    

def validate_fields(data: dict, rules: dict) -> dict:
    """
    Validates the input fields to ensure they exist and are of the correct 
    type and size. This function can handle nested dictionaries for both
    data and rules.

    Args:
        data (dict): Dictionary containing the data to be validated.
        rules (dict): Dictionary containing validation rules.
    
    Returns:
        dict: A dictionary containing information about the validity of each field.
            - "valid": A boolean indicating whether all fields are valid.
            - "errors": A list of error messages.
    """
        
    if data is None or rules is None:
        raise ValueError("Args can't be None.")

    errors = []
    queue = deque([(data, rules, '')])

    while queue:
        current_data, current_rules, parent_key = queue.popleft()

        for field, rule in current_rules.items():
            full_key = f"{parent_key}.{field}" if parent_key else field
            value = current_data.get(field, None)  # Better handle missing field

            if isinstance(rule, dict):
                if 'type' in rule:
                    type_ = rule['type']
                    type_class = string_to_type(type_)
                    max_length = rule.get('max_length')
                    date_format = rule.get('date_format')
                    required = rule.get('required', False)

                    if required and (value is None or value == ''):
                        errors.append(f"{full_key} is required.")
                        continue

                    if value is not None:
                        if type_ == 'datetime':
                            if string_to_datetime(value, date_format) is None:
                                errors.append(f"{full_key} should be a valid datetime.")
                        elif not isinstance(value, type_class):
                            errors.append(f"{full_key} must be of type {type_}.")
                        elif max_length and isinstance(value, str) and len(value) > max_length:
                            errors.append(f"{full_key} can't have more than {max_length} characters.")
                else:
                    # Assume nested dictionary
                    queue.append((value, rule, full_key))

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
