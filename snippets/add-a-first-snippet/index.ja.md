---
title: 初めてのJSON解析スニペット
description: PythonでJSONデータを解析する簡単な例です。
created: 2026-06-13
tags:
  - json
  - python
status: draft
---

PythonでJSONデータを解析するための実用的なスニペットです。この例では、JSON形式の文字列を読み込んで処理する方法を示しています。

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

このコードスニペットには、JSON形式の文字列を受け取り、対応するPython辞書を返す`parse_json`関数が含まれています。この関数は、`json.JSONDecodeError`をキャッチしてエラーを適切に処理します。このエラーは、入力文字列が有効なJSONデータを含まない場合に発生する可能性があります。