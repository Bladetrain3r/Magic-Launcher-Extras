#!/usr/bin/env python3
import json

try:
    print("Loading JSON...")
    with open('./norn_brains/TestNorn_grid.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Writing prettified JSON...")
    with open('export_pretty.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Success! Original: export.json, Prettified: export_pretty.json")
    
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
except Exception as e:
    print(f"Error: {e}")