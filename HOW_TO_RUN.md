# How to Run VatteluttuX

Follow these steps to get your Vatteluttu OCR system up and running.

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## step 1: Setup Backend

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python run.py
   ```
   Server will start at `http://localhost:8000` (API docs at `/docs`).

## Step 2: Setup Frontend

1. Open a **new** terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   Frontend will start at `http://localhost:5173`.

## Step 3: Generating Training Data (First Time Only)

Before training the model, you need to generate synthetic data:

1. Place your Vatteluttu font files (`.ttf` or `.otf`) in `data/fonts/`.
2. Run the generator script:
   ```bash
   python training/generate_data.py --fonts-dir data/fonts --samples 500
   ```
   This will create images in `data/train/` and `data/val/`.

## Step 4: Training the Model

Once data is generated:

1. Run the training script:
   ```bash
   python training/train.py --epochs 20
   ```
   This will save the trained model to `backend/models/vatteluttu_cnn.pth`.

## Step 5: Using the System

1. Open your browser to `http://localhost:5173`.
2. Drag and drop a Vatteluttu inscription image.
3. Click "Recognize Inscription".
4. View the results, copy the Tamil text, or export to JSON/TXT.

## Troubleshooting

- **Backend fails to start**: Check if another service is using port 8000.
- **Frontend can't connect**: Ensure backend is running and `CORS` settings in `backend/app/core/config.py` match your frontend URL.
- **No characters detected**: Try adjusting the `min_char_area` in `backend/app/ocr/pipeline.py` or use higher contrast images.
