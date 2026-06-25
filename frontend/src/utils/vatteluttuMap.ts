/**
 * VatteluttuX - Label Mappings (TypeScript)
 * 
 * Mirror of Python backend mappings.
 * This should be kept in sync with backend/app/core/label_to_char.json
 */

// NOTE: For the full 247-character mapping, this should be loaded from the backend
// or generated from the same source. For now, we provide a subset.

export const LABEL_TO_CHAR: Record<string, string> = {
    // Vowels (Uyir)
    "va_001": "அ",
    "va_002": "ஆ",
    "va_003": "இ",
    "va_004": "ஈ",
    "va_005": "உ",
    "va_006": "ஊ",
    "va_007": "எ",
    "va_008": "ஏ",
    "va_009": "ஐ",
    "va_010": "ஒ",
    "va_011": "ஓ",
    "va_012": "ஔ",
    // Aytham
    "va_013": "ஃ",
    // Pure consonants (sample)
    "va_014": "க்",
    "va_015": "ங்",
    "va_016": "ச்",
    // Consonants with inherent 'a' (sample)
    "va_031": "க",
    "va_032": "ங",
    "va_033": "ச",
    "va_034": "ஞ",
    "va_035": "ட",
    "va_036": "ண",
    "va_037": "த",
    "va_038": "ந",
    "va_039": "ப",
    "va_040": "ம",
    "va_041": "ய",
    "va_042": "ர",
    "va_043": "ல",
    "va_044": "வ",
    "va_045": "ழ",
    "va_046": "ள",
    "va_047": "ற",
    "va_048": "ன",
};

/**
 * Convert an array of labels to Tamil text.
 */
export function labelsToTamil(labels: string[]): string {
    return labels.map(label => LABEL_TO_CHAR[label] || '?').join('');
}

/**
 * Get the Tamil character for a label.
 */
export function labelToChar(label: string): string {
    return LABEL_TO_CHAR[label] || '?';
}
