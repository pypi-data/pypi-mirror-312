import json
from typing import Optional
from collections import deque


def set_nested_value(d, keys, value):
    """Set value in nested dictionary using key path."""
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def get_nested_value(d, keys):
    """Get value from nested dictionary using key path."""
    for key in keys:
        d = d.get(key, {})
    return d


def transform_data(source: dict, transformation_type: str, 
                   json_file: str) -> Optional[dict]:
    """
    Transforma un diccionario de datos de acuerdo a las reglas de 
        transformación definidas en un archivo JSON.

    Args:
        origen (dict): El diccionario de datos original que se quiere 
            transformar.
        tipo (str): El tipo de transformación a aplicar, como se define en el 
            archivo JSON.
        archivo_json (str): Ruta al archivo JSON que contiene las reglas de 
            transformación.

    Returns:
        Optional[dict]: Un nuevo diccionario con los datos transformados, o 
            None si el tipo de transformación no se encuentra.
    
    Raises:
        FileNotFoundError: File json not found.

    Example:
        JSON file ('transformaciones.json'):
        {
            "vendedor": {
                "tel_id": "movil_id",
                "telefono": "movil_numero",
                "latitud": "movil_latitud",
                "longitud": "movil_longitud",
                "salon": "movil_indicador_salon"
            },
            ...
        }

        >>> transform_data({"tel_id": "123", "telefono": "555-1234"}, 
            "vendedor", 'transformaciones.json')
        {'movil_id': '123', 'movil_numero': '555-1234'}
    """
    try:
        with open(json_file, 'r') as f:
            transformations = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {json_file}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON decode error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

    try:
        transformation = transformations.get(transformation_type, {})    
        if not transformation:
            # Raise error if transformation type is not found
            raise ValueError(f"Type {transformation_type} not found in file "\
                             f"{json_file}")
        
        final = {}

        # Process each item in the transformation
        for k_source, k_final in transformation.items():
            source_keys = k_source.split('.')
            final_keys = k_final.split('.')

            # Get the value from the source JSON
            value = get_nested_value(source, source_keys)
            # Set the value in the final JSON
            set_nested_value(final, final_keys, value)
            
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
                    
    return final


def get_json_data(json_data: str, json_file: str) -> Optional[dict]:
    """
    Recupera un conjunto de datos específico de un archivo JSON.

    Args:
        json_data (str): Nombre del conjunto de datos que se quiere recuperar.
        json_file (str): Ruta al archivo JSON que contiene los datos.

    Returns:
        Optional[dict]: Un diccionario con los datos recuperados, o None si el 
            conjunto de datos no se encuentra.

    Raises:
        FileNotFoundError: Si el archivo JSON no se encuentra.
    """
        
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {json_file}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON decode error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
    
    final_data = data.get(json_data, {})
    
    if not final_data:
        # Raise error if transformation type is not found
        raise ValueError(f"Type {json_data} not found in file "\
                f"{json_file}")
    
    try: 
        # Initialize queue and final output
        queue = deque([(final_data, '')])
        processed_data = {}
        
        # Process the queue
        while queue:
            current_data, parent_key = queue.popleft()
            
            # Iterate over each key-value in the current data
            for k, v in current_data.items():
                
                # Check if the value is another dictionary
                if isinstance(v, dict):
                    next_parent_key = f"{parent_key}.{k}" if parent_key else k
                    queue.append((v, next_parent_key))
                
                # Process non-nested values
                else:
                    final_key = f"{parent_key}.{k}" if parent_key else k
                    nested_keys = final_key.split('.')
                    d = processed_data
                    for key in nested_keys[:-1]:
                        d = d.setdefault(key, {})
                    d[nested_keys[-1]] = v
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
      
    return processed_data

