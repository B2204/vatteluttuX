# APPENDICES

---

## Appendix A: Key Source Code Listings

### A.1 Full Preprocessing Pipeline (`backend/app/ml/preprocessing.py`)

```python
"""
VatteluttuX - Image Preprocessing
Functions for preprocessing images before OCR.
"""
import cv2
import numpy as np
from typing import Tuple


def load_image(image_bytes: bytes) -> np.ndarray:
    """Load an image from bytes."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    return img


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert image to grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def denoise(image: np.ndarray, strength: int = 10) -> np.ndarray:
    """Apply denoising to reduce noise in the image."""
    return cv2.fastNlMeansDenoising(image, h=strength)


def adaptive_threshold(image, block_size=11, c=2, invert=False):
    """Apply adaptive thresholding for binarization."""
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresh_type, block_size, c
    )


def otsu_threshold(image, invert=False):
    """Apply Otsu's thresholding for automatic binarization."""
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(image, 0, 255, thresh_type + cv2.THRESH_OTSU)
    return binary


def apply_morphology(image, operation="closing", kernel_size=3,
                     kernel_shape="ellipse", iterations=1):
    """Apply morphological operations."""
    if kernel_shape == "ellipse":
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    elif kernel_shape == "rect":
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (kernel_size, kernel_size))
    else:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if operation == "closing":
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    elif operation == "opening":
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=iterations)


def ensure_white_on_black(binary_image):
    """Ensure binary image has white characters on black background."""
    white_pixels = np.count_nonzero(binary_image)
    white_ratio = white_pixels / binary_image.size
    if white_ratio > 0.5:
        return cv2.bitwise_not(binary_image)
    return binary_image


def preprocess_full(image, denoise_strength=10, use_otsu=True):
    """Full preprocessing pipeline."""
    gray = to_grayscale(image)
    denoised = denoise(gray, denoise_strength)
    if use_otsu:
        binary = otsu_threshold(denoised)
    else:
        binary = adaptive_threshold(denoised)
    binary = ensure_white_on_black(binary)
    return gray, binary
```

---

### A.2 CNN Model Architecture (`backend/app/ml/model.py`)

```python
"""
VatteluttuX - CNN Model Architecture
ResNet-inspired CNN for single character classification.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    """Convolutional block with BatchNorm and ReLU."""
    def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(in_ch, out_ch, kernel_size, stride, padding, bias=False)
        self.bn = nn.BatchNorm2d(out_ch)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class ResidualBlock(nn.Module):
    """Residual block with skip connection."""
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        residual = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return self.relu(out)


class VatteluttuCNN(nn.Module):
    """ResNet-inspired CNN for 247-class Vatteluttu character recognition."""
    def __init__(self, num_classes=247, dropout=0.5):
        super().__init__()
        self.initial = ConvBlock(1, 32)
        self.stage1 = nn.Sequential(ConvBlock(32, 64), ResidualBlock(64), nn.MaxPool2d(2, 2))
        self.stage2 = nn.Sequential(ConvBlock(64, 128), ResidualBlock(128), nn.MaxPool2d(2, 2))
        self.stage3 = nn.Sequential(ConvBlock(128, 256), ResidualBlock(256), nn.MaxPool2d(2, 2))
        self.stage4 = nn.Sequential(ConvBlock(256, 512), ResidualBlock(512), nn.MaxPool2d(2, 2))
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(512, 256), nn.ReLU(inplace=True),
            nn.Dropout(dropout * 0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.initial(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)
```

---

### A.3 Database Model (`backend/app/db/models.py`)

```python
"""
VatteluttuX - Database Models
SQLAlchemy models representing the MySQL database tables.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from app.db.database import Base


class RecognitionHistory(Base):
    """Stores the history of OCR recognition results."""
    __tablename__ = "recognition_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_filename = Column(String(255), nullable=False)
    recognized_text = Column(Text, nullable=False)
    modern_text = Column(Text, nullable=False)
    num_characters = Column(Integer, default=0)
    num_words = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)
    traced_image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

---

## Appendix B: Character Mapping Table (Sample)

The following table shows a representative sample of the 247 Vatteluttu-to-Modern Tamil character mappings. The full mapping is stored in `backend/app/core/label_to_char.json`.

### B.1 Vowels (உயிர் எழுத்து) — 12 Characters

| Label | Modern Tamil | Romanization |
|-------|-------------|-------------|
| va_001 | அ | a |
| va_002 | ஆ | aa |
| va_003 | இ | i |
| va_004 | ஈ | ii |
| va_005 | உ | u |
| va_006 | ஊ | uu |
| va_007 | எ | e |
| va_008 | ஏ | ee |
| va_009 | ஐ | ai |
| va_010 | ஒ | o |
| va_011 | ஓ | oo |
| va_012 | ஔ | au |

### B.2 Aytham — 1 Character

| Label | Modern Tamil | Romanization |
|-------|-------------|-------------|
| va_013 | ஃ | akh |

### B.3 Consonants (Sample) — 18 Characters

| Label | Modern Tamil | Romanization |
|-------|-------------|-------------|
| va_032 | க | ka |
| va_033 | ங | nga |
| va_034 | ச | cha |
| va_035 | ஞ | nya |
| va_036 | ட | ta |
| va_037 | ண | na |
| va_038 | த | tha |
| va_039 | ந | nha |
| va_040 | ப | pa |
| va_041 | ம | ma |
| va_042 | ய | ya |
| va_043 | ர | ra |
| va_044 | ல | la |
| va_045 | வ | va |
| va_046 | ழ | zha |
| va_047 | ள | lla |
| va_048 | ற | rra |
| va_049 | ன | nna |

### B.4 Compound Characters (Sample) — 198 Characters

| Label | Modern Tamil | Formation |
|-------|-------------|-----------|
| va_050 | கா | க + ஆ |
| va_051 | கி | க + இ |
| va_052 | கீ | க + ஈ |
| va_053 | கு | க + உ |
| va_054 | கூ | க + ஊ |
| va_055 | கெ | க + எ |
| va_056 | கே | க + ஏ |
| va_057 | கை | க + ஐ |
| va_058 | கொ | க + ஒ |
| va_059 | கோ | க + ஓ |
| va_060 | கௌ | க + ஔ |
| ... | ... | ... |

*The full table contains 198 compound character entries following the same pattern for all 18 consonants combined with all 11 vowel modifiers.*

---

## Appendix C: Application Screenshots

*The following screenshots should be captured from the running VattalettuX application and inserted into the Word document:*

### Screenshot 1: Home Page — Upload Interface
*Description: The main recognition page showing the drag-and-drop upload area with the VattalettuX header navigation.*

### Screenshot 2: Recognition Results
*Description: After uploading an inscription photo, showing the traced image with colored bounding boxes around detected characters, and the results panel with character-by-character Tamil translation and confidence scores.*

### Screenshot 3: History Page
*Description: The recognition history page showing past OCR sessions with filename, recognized text, number of characters, and timestamp for each record.*

### Screenshot 4: Character Mapping Viewer
*Description: The character map page displaying all 247 Vatteluttu-to-Modern Tamil mappings with category filter buttons (All, Vowels, Consonants, Compounds).*

### Screenshot 5: phpMyAdmin Database View
*Description: The phpMyAdmin interface showing the `vattalettux` database with the `recognition_history` table and its stored records.*

### Screenshot 6: FastAPI Swagger Documentation
*Description: The automatic API documentation page at `/docs` showing all available endpoints with their parameters and response schemas.*

---

## Appendix D: User Manual

### How to Run VattalettuX

**Step 1: Start the Database**
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Verify MySQL is running (status light turns green)

**Step 2: Start the Backend Server**
1. Open a terminal / command prompt
2. Navigate to the project folder:
   ```
   cd "f:\final mca project\VattalettuX"
   ```
3. Activate the Python virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Start the backend:
   ```
   cd backend
   python run.py
   ```
5. Wait for the message "VatteluttuX OCR API Starting..." to appear
6. The API is now running at `http://localhost:8000`

**Step 3: Start the Frontend**
1. Open a new terminal
2. Navigate to the frontend folder:
   ```
   cd "f:\final mca project\VattalettuX\frontend"
   ```
3. Start the development server:
   ```
   npm run dev
   ```
4. The frontend is now running at `http://localhost:5173`

**Step 4: Using the Application**
1. Open a web browser and go to `http://localhost:5173`
2. On the home page, drag and drop an inscription image (or click to browse)
3. Wait approximately 2 seconds for processing
4. View the results:
   - Traced image with bounding boxes
   - Character-by-character translation table
   - Combined Modern Tamil text
5. Navigate to "History" to see past recognition sessions
6. Navigate to "Character Map" to browse all 247 character mappings

**Step 5: Viewing the Database**
1. Open a browser and go to `http://localhost/phpmyadmin`
2. Click on the `vattalettux` database
3. Click on `recognition_history` table to view stored records

---

## Appendix E: Glossary of Technical Terms

This glossary provides simple definitions for the technical terms used throughout this documentation.

| Term | Definition |
|------|-----------|
| **API (Application Programming Interface)** | A set of rules and protocols that allows different software applications to communicate with each other. In VattalettuX, the frontend communicates with the backend through a REST API. |
| **ASGI (Asynchronous Server Gateway Interface)** | A specification for Python web servers and frameworks to handle asynchronous web requests. Uvicorn is an ASGI server used to run FastAPI applications. |
| **Batch Normalization** | A technique used in deep learning to normalize the inputs of each layer. It helps stabilize training and allows using higher learning rates. |
| **Binary Image** | An image where every pixel is either black (0) or white (255). Binary images are used for character detection because they clearly separate foreground (characters) from background. |
| **Bounding Box** | A rectangle that encloses a detected character in an image. Defined by four values: x-coordinate, y-coordinate, width, and height. |
| **CNN (Convolutional Neural Network)** | A type of deep learning model specifically designed for processing image data. CNNs use convolutional filters that slide across an image to detect visual features like edges, curves, and shapes. |
| **Connected Component Analysis (CCA)** | An image processing algorithm that identifies groups of connected foreground pixels. Each group is treated as a potential character region. |
| **Convex Hull** | The smallest convex shape that completely encloses a set of points (or a contour). Used to calculate solidity. |
| **CORS (Cross-Origin Resource Sharing)** | A security mechanism that controls which websites can make requests to a web server. VattalettuX configures CORS to allow the React frontend (port 5173) to access the FastAPI backend (port 8000). |
| **CRUD (Create, Read, Update, Delete)** | The four basic database operations. VattalettuX uses Create (save recognition), Read (view history), and Delete (remove history record). |
| **Dropout** | A regularization technique where random neurons are temporarily "turned off" during training. This prevents the model from relying too heavily on any single neuron and reduces overfitting. |
| **Epoch** | One complete pass through the entire training dataset during model training. VattalettuX was trained for 100 epochs. |
| **Epigraphist** | A specialist trained in reading and interpreting ancient inscriptions (epigraphy). |
| **FastAPI** | A modern, high-performance Python web framework for building REST APIs. It provides automatic documentation, data validation, and async support. |
| **Feature Map** | The output of a convolutional layer in a CNN. Each feature map captures a specific visual pattern (edge, corner, texture, etc.) at different locations in the image. |
| **F1-Score** | A metric that combines Precision and Recall into a single number. It is the harmonic mean of Precision and Recall: F1 = 2 × (Precision × Recall) / (Precision + Recall). |
| **Global Average Pooling** | A technique that reduces a 2D feature map to a single number by taking the average of all values. Used to convert spatial feature maps into a 1D feature vector for classification. |
| **Grayscale** | An image represented using a single channel where each pixel has a brightness value from 0 (black) to 255 (white). |
| **He (Kaiming) Initialization** | A weight initialization method for neural networks that sets initial weights based on the number of input connections. Specifically designed for networks using ReLU activation. |
| **Histogram Equalization** | An image processing technique that improves contrast by redistributing the pixel intensity values across the full brightness range. |
| **IoU (Intersection over Union)** | A metric that measures the overlap between two bounding boxes. Calculated as the area of intersection divided by the area of union. Used to merge overlapping detections. |
| **JSON (JavaScript Object Notation)** | A lightweight text format for storing and exchanging structured data. Used for API communication and character mapping storage. |
| **Learning Rate** | A number that controls how much the model's weights are adjusted during each training step. Too high = unstable training; too low = very slow training. |
| **Max Pooling** | An operation that reduces the spatial size of feature maps by taking the maximum value in each small region. Helps the model become invariant to small spatial shifts. |
| **Morphological Operations** | Image processing operations that modify the shape and structure of binary image regions. Include dilation (expand), erosion (shrink), opening (remove noise), and closing (fill gaps). |
| **MySQL** | An open-source relational database management system. VattalettuX uses MySQL to store recognition history. |
| **OCR (Optical Character Recognition)** | Technology that converts images of text into machine-readable digital text. |
| **ORM (Object-Relational Mapping)** | A programming technique that maps database tables to programming language objects. SQLAlchemy is the ORM used in VattalettuX. |
| **Otsu's Threshold** | An automatic binarization method that determines the optimal threshold value by analyzing the image's brightness histogram. |
| **Overfitting** | When a model performs well on training data but poorly on new, unseen data. Overfitting means the model has memorized the training examples rather than learning general patterns. |
| **Precision** | The proportion of detected characters that are actual characters (not noise). Precision = True Positives / (True Positives + False Positives). |
| **Recall** | The proportion of actual characters that were successfully detected. Recall = True Positives / (True Positives + False Negatives). |
| **ReLU (Rectified Linear Unit)** | An activation function used in neural networks that outputs the input value if positive, or zero if negative. It is the most commonly used activation function in modern deep learning. |
| **Residual Block** | A building block of ResNet architectures that adds the input directly to the output of two convolution layers (skip connection). This helps train deeper networks. |
| **REST (Representational State Transfer)** | An architectural style for designing web APIs. REST APIs use standard HTTP methods (GET, POST, DELETE) and URL-based resource addressing. |
| **ResNet (Residual Network)** | A CNN architecture that introduced skip connections (residual connections) to enable training of very deep networks. VatteluttuCNN is inspired by ResNet. |
| **Segmentation** | The process of dividing an image into meaningful regions — in OCR, this means isolating individual characters from a text image. |
| **Skip Connection** | A connection in a neural network that bypasses one or more layers by adding the input directly to the output. Helps gradients flow during backpropagation. |
| **Softmax** | A mathematical function that converts a vector of raw model outputs (logits) into a probability distribution where all values sum to 1. |
| **Solidity** | The ratio of a component's area to its convex hull area. High solidity indicates a compact, solid shape (likely a character). Low solidity indicates a hollow or irregular shape (likely noise). |
| **SQLAlchemy** | A Python library for database operations that provides both a SQL expression language and an ORM. Used in VattalettuX for MySQL database interaction. |
| **Synthetic Data** | Training data that is artificially generated rather than collected from real-world examples. VattalettuX generates synthetic character images using font rendering and augmentation. |
| **Top-1 Accuracy** | The percentage of test images where the model's single most confident prediction is correct. |
| **Top-5 Accuracy** | The percentage of test images where the correct answer is among the model's five most confident predictions. |
| **TypeScript** | A programming language that extends JavaScript with static type checking. Used in VattalettuX's React.js frontend for better code reliability. |
| **Unicode** | An international standard for encoding text characters from all writing systems. Tamil Unicode characters use code points in the range U+0B80 to U+0BFF. |
| **Uvicorn** | A high-performance ASGI server for Python web applications. Used to serve the FastAPI backend. |
| **Vatteluttu (வட்டெழுத்து)** | An ancient Tamil script meaning "round letters," used from approximately the 3rd to 12th century CE. |
| **Vertical Projection Profile** | A histogram showing the number of foreground (white) pixels in each column of a binary image. Valleys in the profile indicate potential spaces between characters. |
| **Vite** | A modern JavaScript build tool that provides a fast development server and optimized production builds. Used for the React.js frontend. |

---

## Appendix F: Environment Configuration

### F.1 Backend Environment Variables

The backend server uses the following environment variables, configured through a `.env` file or system environment:

| Variable | Default Value | Description |
|----------|--------------|-------------|
| `DATABASE_URL` | `mysql+pymysql://root:@localhost/vattalettux` | MySQL connection string |
| `CORS_ORIGINS` | `*` | Allowed frontend origins for CORS |
| `MODEL_PATH` | `app/core/model_weights.pth` | Path to trained CNN model weights |
| `LABEL_MAP_PATH` | `app/core/label_to_char.json` | Path to character mapping JSON |
| `MEDIA_DIR` | `media` | Directory for uploaded images |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

### F.2 MySQL Database Configuration

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `3306` |
| Database Name | `vattalettux` |
| Username | `root` |
| Password | *(blank — default XAMPP)* |
| Character Set | `utf8mb4` (for Tamil Unicode support) |
| Collation | `utf8mb4_unicode_ci` |

### F.3 Project Directory Structure

```
VattalettuX/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py          # API endpoint definitions
│   │   │   └── schemas.py         # Pydantic response models
│   │   ├── core/
│   │   │   ├── config.py          # Application settings
│   │   │   ├── label_to_char.json # Character mapping data
│   │   │   └── model_weights.pth  # Trained CNN model
│   │   ├── db/
│   │   │   ├── database.py        # SQLAlchemy engine & session
│   │   │   ├── models.py          # Database table definitions
│   │   │   └── crud.py            # Database operations
│   │   ├── ml/
│   │   │   ├── model.py           # CNN architecture definition
│   │   │   ├── preprocessing.py   # Image preprocessing functions
│   │   │   └── mapping.py         # Label-to-Tamil mapping
│   │   ├── ocr/
│   │   │   ├── pipeline.py        # End-to-end OCR pipeline
│   │   │   └── segmentation.py    # Character segmentation
│   │   └── main.py                # FastAPI app initialization
│   ├── media/                     # Uploaded & traced images
│   ├── requirements.txt           # Python dependencies
│   └── run.py                     # Server startup script
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx         # Navigation header
│   │   │   ├── RecognitionPage.tsx # Main recognition page
│   │   │   ├── UploadPanel.tsx    # Image upload component
│   │   │   ├── ResultsDisplay.tsx # Results display component
│   │   │   ├── HistoryPage.tsx    # Recognition history
│   │   │   ├── CharacterMappingViewer.tsx  # Character map
│   │   │   └── CharacterTable.tsx # Character table component
│   │   ├── utils/
│   │   │   └── api.ts             # API communication utilities
│   │   ├── App.tsx                # Main application component
│   │   └── main.tsx               # Application entry point
│   ├── package.json               # Node.js dependencies
│   └── vite.config.ts             # Vite build configuration
├── training/
│   ├── generate_data.py           # Synthetic data generation
│   ├── dataset.py                 # PyTorch dataset loader
│   └── train.py                   # Model training script
├── docs/
│   ├── chapters/                  # Documentation chapters
│   └── Project_Documentation.md   # Original project docs
└── README.md                      # Project readme
```

---

