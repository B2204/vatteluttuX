"""
Complete Vatteluttu character mapping based on Tamil script structure.

Tamil script structure:
- 12 Uyir (vowels): அ ஆ இ ஈ உ ஊ எ ஏ ஐ ஒ ஓ ஔ
- 18 Mei (consonants): க ங ச ஞ ட ண த ந ப ம ய ர ல வ ழ ள ற ன
- 216 Uyirmei (consonant + vowel combinations)
- 1 Aytham: ஃ

Total standard: 12 + 18 + 216 + 1 = 247 characters
"""
import json

# Tamil vowels (Uyir)
VOWELS = ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ']

# Tamil consonants (Mei) - pure form with pulli
CONSONANTS = ['க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ப', 'ம', 'ய', 'ர', 'ல', 'வ', 'ழ', 'ள', 'ற', 'ன']

# Vowel marks (maatraikal) for combining with consonants
# These are added to consonants to form uyirmei letters
VOWEL_MARKS = {
    'அ': '',      # inherent 'a' - no mark
    'ஆ': 'ா',     # aa
    'இ': 'ி',     # i
    'ஈ': 'ீ',     # ii
    'உ': 'ு',     # u
    'ஊ': 'ூ',     # uu
    'எ': 'ெ',     # e
    'ஏ': 'ே',     # ee
    'ஐ': 'ை',     # ai
    'ஒ': 'ொ',     # o
    'ஓ': 'ோ',     # oo
    'ஔ': 'ௌ',     # au
}

# Transliteration mappings
VOWEL_TRANSLIT = {
    'அ': 'a', 'ஆ': 'aa', 'இ': 'i', 'ஈ': 'ii', 
    'உ': 'u', 'ஊ': 'uu', 'எ': 'e', 'ஏ': 'ee',
    'ஐ': 'ai', 'ஒ': 'o', 'ஓ': 'oo', 'ஔ': 'au'
}

CONSONANT_TRANSLIT = {
    'க': 'k', 'ங': 'ng', 'ச': 'ch', 'ஞ': 'nj',
    'ட': 't', 'ண': 'n', 'த': 'th', 'ந': 'nh',
    'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
    'ல': 'l', 'வ': 'v', 'ழ': 'zh', 'ள': 'l',
    'ற': 'r', 'ன': 'n'
}

def create_full_character_map():
    character_map = {}
    label_idx = 1
    
    # 1. Add vowels (Uyir) - 12 characters
    for vowel in VOWELS:
        label = f"va_{label_idx:03d}"
        character_map[label] = {
            "modern_tamil": vowel,
            "category": "vowel",
            "transliteration": VOWEL_TRANSLIT[vowel],
            "description": f"Vowel {vowel}"
        }
        label_idx += 1
    
    # 2. Add Aytham - 1 character
    label = f"va_{label_idx:03d}"
    character_map[label] = {
        "modern_tamil": "ஃ",
        "category": "aytham",
        "transliteration": "h",
        "description": "Aytham (visarga)"
    }
    label_idx += 1
    
    # 3. Add pure consonants (with pulli/virama) - 18 characters
    # These represent the consonant without any vowel sound
    for consonant in CONSONANTS:
        label = f"va_{label_idx:03d}"
        pure_consonant = consonant + '்'  # Add pulli (virama)
        character_map[label] = {
            "modern_tamil": pure_consonant,
            "category": "pure_consonant",
            "transliteration": CONSONANT_TRANSLIT[consonant],
            "description": f"Pure consonant {consonant}் (with pulli)"
        }
        label_idx += 1
    
    # 4. Add consonants with inherent 'a' (ka, nga, cha, etc.) - 18 characters
    for consonant in CONSONANTS:
        label = f"va_{label_idx:03d}"
        character_map[label] = {
            "modern_tamil": consonant,
            "category": "consonant",
            "transliteration": CONSONANT_TRANSLIT[consonant] + "a",
            "description": f"Consonant {consonant} (with inherent a)"
        }
        label_idx += 1
    
    # 5. Add Uyirmei (consonant + vowel combinations) - 18 consonants × 11 vowels = 198 characters
    # Skip 'அ' as it's the inherent vowel already covered above
    for consonant in CONSONANTS:
        for vowel in VOWELS[1:]:  # Skip 'அ' as it's the inherent vowel
            label = f"va_{label_idx:03d}"
            vowel_mark = VOWEL_MARKS[vowel]
            combined = consonant + vowel_mark
            
            character_map[label] = {
                "modern_tamil": combined,
                "category": "uyirmei",
                "base_consonant": consonant,
                "vowel_mark": vowel,
                "transliteration": CONSONANT_TRANSLIT[consonant] + VOWEL_TRANSLIT[vowel],
                "description": f"{consonant} + {vowel}"
            }
            label_idx += 1
    
    print(f"Total characters: {len(character_map)}")
    print(f"  Vowels: 12")
    print(f"  Aytham: 1")
    print(f"  Pure consonants (with pulli): 18")
    print(f"  Consonants (with inherent a): 18")
    print(f"  Uyirmei: 198")
    print(f"  Total: 12 + 1 + 18 + 18 + 198 = 247")
    
    return character_map



def save_character_map(character_map):
    # Save as JSON
    output_path = r'F:\final mca project\VattalettuX\backend\app\core\character_map.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(character_map, f, ensure_ascii=False, indent=2)
    print(f"\nSaved character_map.json to: {output_path}")
    
    # Create a simpler LABEL_TO_CHAR mapping for quick lookups
    label_to_char = {label: data['modern_tamil'] for label, data in character_map.items()}
    label_to_char_path = r'F:\final mca project\VattalettuX\backend\app\core\label_to_char.json'
    with open(label_to_char_path, 'w', encoding='utf-8') as f:
        json.dump(label_to_char, f, ensure_ascii=False, indent=2)
    print(f"Saved label_to_char.json to: {label_to_char_path}")
    
    # Create summary text file
    summary_path = r'F:\final mca project\VattalettuX\docs\character_map_complete.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("VatteluttuX Complete Character Map\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total characters: {len(character_map)}\n\n")
        
        f.write("VOWELS (Uyir) - 12 characters\n")
        f.write("-" * 50 + "\n")
        for label, data in character_map.items():
            if data['category'] == 'vowel':
                f.write(f"{label}: {data['modern_tamil']} ({data['transliteration']})\n")
        
        f.write("\nAYTHAM - 1 character\n")
        f.write("-" * 50 + "\n")
        for label, data in character_map.items():
            if data['category'] == 'aytham':
                f.write(f"{label}: {data['modern_tamil']} ({data['transliteration']})\n")
        
        f.write("\nCONSONANTS (Mei with inherent 'a') - 18 characters\n")
        f.write("-" * 50 + "\n")
        for label, data in character_map.items():
            if data['category'] == 'consonant':
                f.write(f"{label}: {data['modern_tamil']} ({data['transliteration']})\n")
        
        f.write("\nUYIRMEI (Consonant + Vowel combinations) - 198 characters\n")
        f.write("-" * 50 + "\n")
        for label, data in character_map.items():
            if data['category'] == 'uyirmei':
                f.write(f"{label}: {data['modern_tamil']} ({data['transliteration']}) - {data['description']}\n")
    
    print(f"Saved summary to: {summary_path}")


if __name__ == "__main__":
    import os
    os.makedirs(r'F:\final mca project\VattalettuX\backend\app\core', exist_ok=True)
    
    char_map = create_full_character_map()
    save_character_map(char_map)
