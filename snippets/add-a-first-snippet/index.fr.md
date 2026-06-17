---
title: Premier extrait de parsing JSON
description: Un exemple simple de parsing de données JSON en Python.
created: 2026-06-13
tags:
  - json
  - python
status: draft
---

Voici un extrait pratique pour le parsing de données JSON en Python. Cet exemple montre comment lire et traiter des chaînes formatées en JSON.

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

Cet extrait de code inclut une fonction `parse_json` qui prend une chaîne formatée en JSON et retourne le dictionnaire Python correspondant. Il gère les erreurs correctement en attrapant `json.JSONDecodeError`, qui peut survenir si la chaîne d'entrée ne contient pas de données JSON valides.