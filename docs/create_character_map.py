"""
Script to create the final character_map.json from extracted PDF data.
This creates the single source of truth for Vatteluttu → Modern Tamil mappings.
"""
import json
import re

def create_character_map():
    # Load raw mappings
    with open(r'F:\final mca project\VattalettuX\docs\raw_mappings.json', 'r', encoding='utf-8') as f:
        raw_mappings = json.load(f)
    
    character_map = {}
    
    # Tamil vowel chart for reference
    tamil_vowels = {
        'அ': 'a', 'ஆ': 'aa', 'இ': 'i', 'ஈ': 'ii', 
        'உ': 'u', 'ஊ': 'uu', 'எ': 'e', 'ஏ': 'ee',
        'ஐ': 'ai', 'ஒ': 'o', 'ஓ': 'oo', 'ஔ': 'au'
    }
    
    # Tamil consonants for reference
    tamil_consonants = {
        'க': 'ka', 'ங': 'nga', 'ச': 'ca', 'ஞ': 'nya',
        'ட': 'ta', 'ண': 'na', 'த': 'tha', 'ந': 'nha',
        'ப': 'pa', 'ம': 'ma', 'ய': 'ya', 'ர': 'ra',
        'ல': 'la', 'வ': 'va', 'ழ': 'zha', 'ள': 'la2',
        'ற': 'rra', 'ன': 'nna'
    }
    
    for idx, mapping in enumerate(raw_mappings):
        page = mapping['page']
        raw_content = mapping['raw_content']
        
        # Label as va_001, va_002, etc.
        label = f"va_{idx + 1:03d}"
        
        # Parse the raw content to extract Brahmi and Tamil characters
        brahmi_char = None
        modern_tamil = None
        
        for content in raw_content:
            # Extract characters
            chars = list(content.replace(' ', ''))
            
            for char in chars:
                code = ord(char)
                # Brahmi range: U+11000 to U+1107F
                if 0x11000 <= code <= 0x1107F:
                    if brahmi_char is None:
                        brahmi_char = char
                    else:
                        brahmi_char += char  # Combined characters
                # Tamil range: U+0B80 to U+0BFF
                elif 0x0B80 <= code <= 0x0BFF:
                    if modern_tamil is None:
                        modern_tamil = char
                    elif len(modern_tamil) < 3:  # Limit to reasonable length
                        modern_tamil += char
        
        # Get transliteration
        translit = ""
        if modern_tamil:
            if modern_tamil in tamil_vowels:
                translit = tamil_vowels[modern_tamil]
            elif modern_tamil in tamil_consonants:
                translit = tamil_consonants[modern_tamil]
            elif len(modern_tamil) > 0:
                first_char = modern_tamil[0]
                if first_char in tamil_consonants:
                    translit = tamil_consonants[first_char]
        
        character_map[label] = {
            "vatteluttu": brahmi_char if brahmi_char else "",
            "modern_tamil": modern_tamil if modern_tamil else "",
            "transliteration": translit,
            "page_ref": page
        }
    
    # Sort by label
    sorted_map = dict(sorted(character_map.items(), key=lambda x: int(x[0].split('_')[1])))
    
    # Save the character map
    output_path = r'F:\final mca project\VattalettuX\backend\app\core\character_map.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, ensure_ascii=False, indent=2)
    
    # Also create a summary
    summary_path = r'F:\final mca project\VattalettuX\docs\character_map_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Vatteluttu Character Map Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total characters: {len(sorted_map)}\n\n")
        f.write(f"{'Label':<10} {'Vatteluttu':<15} {'Modern Tamil':<15} {'Transliteration':<15}\n")
        f.write("-" * 55 + "\n")
        for label, data in sorted_map.items():
            f.write(f"{label:<10} {data['vatteluttu']:<15} {data['modern_tamil']:<15} {data['transliteration']:<15}\n")
    
    print(f"Created character_map.json with {len(sorted_map)} characters")
    print(f"Saved to: {output_path}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    import os
    # Create directory if needed
    os.makedirs(r'F:\final mca project\VattalettuX\backend\app\core', exist_ok=True)
    create_character_map()
