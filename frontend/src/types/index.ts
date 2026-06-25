/**
 * VatteluttuX - TypeScript Type Definitions
 */

export interface CharacterPrediction {
  label: string;
  modern_tamil: string;
  confidence: number;
  bbox: [number, number, number, number]; // [x, y, width, height]
  transliteration?: string;
}

export interface WordPrediction {
  text: string;
  labels: string[];
  confidence: number;
  bbox: [number, number, number, number];
  is_validated: boolean;
  validation_warnings: string[];
  num_characters: number;
}

export interface RecognitionResponse {
  recognized_text: string;
  modern_text: string;
  characters: CharacterPrediction[];
  words: WordPrediction[];
  traced_image_path: string;
  image_width: number;
  image_height: number;
  warnings: string[];
  num_words: number;
  num_characters: number;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  num_classes: number;
  version: string;
}

export interface HistoryItem {
  id: number;
  original_filename: string;
  recognized_text: string;
  modern_text: string;
  num_characters: number;
  num_words: number;
  avg_confidence: number;
  traced_image_path: string | null;
  created_at: string;
}

export type RecognitionState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: RecognitionResponse }
  | { status: 'error'; message: string };
