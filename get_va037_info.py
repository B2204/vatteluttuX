import json

# Path to the character map
path = r'f:\final mca project\VattalettuX\backend\app\core\character_map.json'

try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        info = data.get('va_037')
        
    if info:
        output = {
            "Label": "va_037",
            "Tamil": info.get("modern_tamil"),
            "Category": info.get("category"),
            "Transliteration": info.get("transliteration"),
            "Description": info.get("description")
        }
        with open('va037_info.json', 'w', encoding='utf-8') as f2:
            json.dump(output, f2, indent=2, ensure_ascii=False)
        print("Success: Info saved to va037_info.json")
    else:
        print("Error: va_037 not found in character map")
except Exception as e:
    print(f"Error: {e}")
