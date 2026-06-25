# VatteluttuX Backend

A FastAPI backend for Vatteluttu OCR recognition.

## Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

## API Endpoints

### OCR & Health
- `GET /health` - Health check with model status
- `POST /recognize` - OCR recognition from image

### Character Mapping
- `GET /labels` - Get all character labels and their Tamil mappings
- `GET /labels/{label}` - Get detailed info for a specific label (e.g., `va_001`)
- `GET /characters?category=vowel` - Get characters filtered by category (vowel, consonant, uyirmei, etc.)
- `GET /character-map` - Get complete character dataset with statistics and categories

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── api/
│   │   ├── routes.py    # API endpoints
│   │   └── schemas.py   # Pydantic models
│   ├── core/
│   │   ├── config.py    # Settings
│   │   ├── character_map.json
│   │   └── label_mappings.py
│   ├── ml/
│   │   ├── model.py     # CNN architecture
│   │   ├── inference.py # Model inference
│   │   └── preprocessing.py
│   ├── ocr/
│   │   ├── pipeline.py  # OCR pipeline
│   │   ├── segmentation.py
│   │   └── traced_image.py
│   └── media/           # Output traced images
├── models/              # Saved model weights
├── requirements.txt
└── run.py
```
