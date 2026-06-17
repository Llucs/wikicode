---
title: Erstes JSON-Parsing-Snippet
description: Ein einfaches Beispiel für das Parsen von JSON-Daten in Python.
created: 2026-06-13
tags:
  - json
  - python
status: draft
---

Hier ist ein praktisches Snippet zum Parsen von JSON-Daten in Python. Dieses Beispiel zeigt, wie man JSON-formatierte Strings liest und verarbeitet.

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

Dieses Code-Snippet enthält eine Funktion `parse_json`, die einen JSON-formatierten String entgegennimmt und das entsprechende Python-Dictionary zurückgibt. Sie behandelt Fehler elegant, indem sie `json.JSONDecodeError` abfängt, der auftreten kann, wenn der Eingabestring keine gültigen JSON-Daten enthält.