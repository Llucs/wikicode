---
title: Primer fragmento de análisis JSON
description: Un ejemplo sencillo de análisis de datos JSON en Python.
created: 2026-06-13
tags:
  - json
  - python
status: draft
---

Aquí tienes un fragmento práctico para analizar datos JSON en Python. Este ejemplo demuestra cómo leer y procesar cadenas con formato JSON.

```python
# Importing the necessary library
import json

def parse_json(json_string):
    """
    Parses a JSON string into a Python dictionary.
    
    Args:
        json_string (str): A JSON-formatted string.
        
    Returns:
        dict: The parsed data as a Python dictionary.
    """
    try:
        # Parse the JSON string to a Python dictionary
        result = json.loads(json_string)
        return result
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None

# Example usage of the function
json_data = '{"name": "John Doe", "age": 30, "city": "New York"}'
parsed_data = parse_json(json_data)
print(parsed_data)

if parsed_data is not None:
    print(f"Parsed JSON: {parsed_data}")
```

Este fragmento de código incluye una función `parse_json` que toma una cadena con formato JSON y devuelve el diccionario de Python correspondiente. Maneja los errores de manera elegante capturando `json.JSONDecodeError`, que puede ocurrir si la cadena de entrada no contiene datos JSON válidos.