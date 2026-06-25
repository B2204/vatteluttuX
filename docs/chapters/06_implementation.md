# CHAPTER 5: IMPLEMENTATION

---

## 5.1 Introduction

This chapter describes how each module of VattalettuX was actually built. We cover the technology stack, development environment setup, and then walk through the implementation of each module with key code snippets and explanations. The code is written in a clear and modular style, with each file having a single well-defined responsibility.

---

## 5.2 Technology Stack

The following table summarizes every technology used in the project, its version, and the specific role it plays:

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.10+ | Backend logic, ML model, image processing |
| **Language** | TypeScript | 5.9 | Frontend UI logic with type safety |
| **Deep Learning** | PyTorch | 2.1+ | CNN model definition, training, and inference |
| **Deep Learning** | TorchVision | 0.16+ | Image transforms and data augmentation |
| **Web Framework** | FastAPI | 0.109+ | REST API server with automatic OpenAPI docs |
| **ASGI Server** | Uvicorn | 0.27+ | High-performance async Python web server |
| **Image Processing** | OpenCV | 4.9+ | Preprocessing, segmentation, morphology |
| **Image I/O** | Pillow (PIL) | 10.0+ | Image loading, conversion, and saving |
| **Numerical** | NumPy | 1.26+ | Array operations for image data |
| **Database ORM** | SQLAlchemy | 2.0+ | Object-relational mapping for MySQL |
| **MySQL Driver** | PyMySQL | 1.1+ | Python connector for MySQL databases |
| **Validation** | Pydantic | 2.5+ | Request/response data validation |
| **Frontend Framework** | React.js | 19.2 | Component-based UI rendering |
| **Build Tool** | Vite | 7.2+ | Fast development server and production bundler |
| **Database** | MySQL | 8.0+ | Persistent storage for recognition history |
| **DB Management** | phpMyAdmin (XAMPP) | Latest | Visual database administration tool |

---

## 5.3 Development Environment Setup

### 5.3.1 Prerequisites

The following software must be installed on the development machine:

1. **Python 3.10 or higher** — Download from python.org
2. **Node.js 18 or higher** — Download from nodejs.org
3. **XAMPP** — For running MySQL server and phpMyAdmin
4. **Git** — For version control

### 5.3.2 Backend Setup

The backend dependencies are managed via a `requirements.txt` file:

```
# FastAPI and Server
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6

# Image Processing
opencv-python>=4.9.0.80
Pillow>=10.0.0
numpy>=1.26.0

# Machine Learning
torch>=2.1.2
torchvision>=0.16.2

# Database
sqlalchemy>=2.0.0
pymysql>=1.1.0

# Utilities
pydantic>=2.5.3
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
```

To set up the backend:

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the backend server
cd backend
python run.py
```

### 5.3.3 Frontend Setup

The frontend uses Node.js with npm for package management:

```bash
# Install frontend dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

### 5.3.4 Database Setup

1. Open XAMPP Control Panel and start MySQL.
2. Open phpMyAdmin at `http://localhost/phpmyadmin`.
3. Create a new database called `vattalettux`.
4. The application automatically creates the required tables when it starts.

---

## 5.4 Module-wise Implementation

### 5.4.1 Image Preprocessing Module

**File**: `backend/app/ml/preprocessing.py`

This module handles all image preprocessing operations needed to prepare raw inscription photographs for character segmentation. The preprocessing pipeline consists of four main steps applied in sequence.

**Step 1: Loading and Grayscale Conversion**

The first step converts the input image to grayscale, since colour information is not needed for character recognition:

```python
def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert image to grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image
```

This function uses OpenCV's `cvtColor` function to convert a 3-channel BGR image to a single-channel grayscale image. The `if` check ensures the function works safely even if the image is already in grayscale format.

**Step 2: Denoising**

Stone inscription photographs contain significant noise from surface texture, dust, and camera artifacts. We apply Non-Local Means Denoising to reduce this noise:

```python
def denoise(image: np.ndarray, strength: int = 10) -> np.ndarray:
    """Apply denoising to reduce noise in the image."""
    return cv2.fastNlMeansDenoising(image, h=strength)
```

The `h` parameter controls the denoising strength. Higher values remove more noise but may also blur fine details of the characters.

**Step 3: Adaptive Thresholding (Binarization)**

Binarization converts the grayscale image into a pure black-and-white image. We use adaptive thresholding because stone inscriptions rarely have uniform lighting:

```python
def adaptive_threshold(
    image: np.ndarray,
    block_size: int = 11,
    c: int = 2,
    invert: bool = False
) -> np.ndarray:
    """Apply adaptive thresholding for binarization."""
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresh_type, block_size, c
    )
```

Unlike global thresholding (which uses one brightness cutoff for the entire image), adaptive thresholding calculates a local threshold for each pixel based on the average brightness of a surrounding neighbourhood. The `block_size` parameter defines the size of this neighbourhood, and `c` is a small correction constant.

We also provide Otsu's thresholding as an alternative:

```python
def otsu_threshold(image: np.ndarray, invert: bool = False) -> np.ndarray:
    """Apply Otsu's thresholding for automatic binarization."""
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(
        image, 0, 255, thresh_type + cv2.THRESH_OTSU
    )
    return binary
```

Otsu's method automatically determines the optimal threshold value by analysing the image histogram.

**Step 4: Morphological Noise Removal**

After binarization, small pits and cracks on the stone surface may appear as noise dots. We remove these using morphological operations:

```python
def apply_morphology(
    image: np.ndarray,
    operation: str = "closing",
    kernel_size: int = 3,
    kernel_shape: str = "ellipse",
    iterations: int = 1
) -> np.ndarray:
    """Apply morphological operations to repair broken
    strokes or remove noise."""

    # Create structuring element
    if kernel_shape == "ellipse":
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
        )
    # ... (other shapes: rect, cross)

    # Apply operation
    if operation == "closing":
        # Dilation followed by Erosion — fills small holes
        result = cv2.morphologyEx(
            image, cv2.MORPH_CLOSE, kernel, iterations=iterations
        )
    elif operation == "opening":
        # Erosion followed by Dilation — removes small noise
        result = cv2.morphologyEx(
            image, cv2.MORPH_OPEN, kernel, iterations=iterations
        )
    return result
```

**Morphological closing** (dilation then erosion) connects broken strokes — useful for characters that have been partially eroded. **Morphological opening** (erosion then dilation) removes small noise particles while keeping the main character shapes intact.

**Full Preprocessing Pipeline**

All these steps are combined into a single function:

```python
def preprocess_full(
    image: np.ndarray,
    denoise_strength: int = 10,
    use_otsu: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """Full preprocessing pipeline."""
    gray = to_grayscale(image)
    denoised = denoise(gray, denoise_strength)

    if use_otsu:
        binary = otsu_threshold(denoised, invert=False)
    else:
        binary = adaptive_threshold(denoised, invert=False)

    # Auto-detect polarity and ensure white-on-black
    binary = ensure_white_on_black(binary)

    return gray, binary
```

The `ensure_white_on_black()` function checks whether the characters are darker or lighter than the background and automatically inverts the image if necessary. This makes the pipeline robust to both positive and negative inscription images.

---

### 5.4.2 Character Segmentation Module

**File**: `backend/app/ocr/segmentation.py`

Once the image has been cleaned and binarized, we need to locate each individual character. This module implements character segmentation using Connected Component Analysis (CCA) along with several filtering and merging strategies.

**BoundingBox Data Class**

We defined a simple data class to represent the rectangular region around each detected character:

```python
@dataclass
class BoundingBox:
    """Bounding box for a detected character."""
    x: int
    y: int
    width: int
    height: int

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    def crop(self, image: np.ndarray) -> np.ndarray:
        """Extract the region from an image."""
        return image[self.y:self.y + self.height,
                     self.x:self.x + self.width]
```

**Connected Component Analysis**

The core segmentation function uses OpenCV's `connectedComponentsWithStats` to find groups of connected foreground pixels:

```python
def find_connected_components(
    binary_image: np.ndarray,
    min_area: int = 100,
    max_area: int = None,
    horizontal_merge_gap: int = 10
) -> List[BoundingBox]:
    """Find connected components and merge those
    within a horizontal gap."""

    num_labels, labels, stats, centroids = \
        cv2.connectedComponentsWithStats(
            binary_image, connectivity=8
        )

    initial_boxes = []
    for i in range(1, num_labels):  # Skip background (0)
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]

        if area >= 3 and area <= max_area:
            initial_boxes.append(BoundingBox(x, y, w, h))
    # ... merge nearby components ...
    return merged_boxes
```

After initial detection, several filtering and processing steps are applied:

1. **Noise Filtering** (`filter_noise_components`): Removes components with very low solidity (ratio of component area to convex hull area) or extreme aspect ratios. This eliminates cracks, scratches, and surface imperfections.

2. **Median Size Filtering** (`filter_by_median_size`): Removes components that are much smaller than the median character size — these are typically small noise artifacts.

3. **Wide Box Splitting** (`split_wide_boxes`): Detects bounding boxes that are much wider than the median width (likely two merged characters) and splits them at valley points in the vertical projection profile.

4. **Overlap Merging** (`merge_overlapping_boxes`): Uses IoU (Intersection over Union) to detect and merge overlapping bounding boxes.

5. **Reading Order Sorting** (`sort_boxes_reading_order`): Groups characters into rows based on their vertical centre positions and sorts each row left-to-right.

**Main Segmentation Function**

```python
def segment_characters(
    binary_image: np.ndarray,
    min_area: int = 100,
    apply_morphology: bool = True,
    filter_noise: bool = True,
    min_solidity: float = 0.3
) -> List[BoundingBox]:
    """Segment characters from a binary image."""
    # Apply morphological closing for broken strokes
    if apply_morphology:
        processed_image = morph_op(
            binary_image, operation="closing",
            kernel_size=3, kernel_shape="ellipse"
        )

    # Find connected components
    boxes = find_connected_components(
        processed_image, min_area=min_area
    )

    # Filter noise, median size, split wide, merge overlap
    boxes = filter_noise_components(processed_image, boxes)
    boxes = filter_by_median_size(boxes, min_ratio=0.3)
    boxes = split_wide_boxes(processed_image, boxes)
    boxes = merge_overlapping_boxes(boxes)

    # Sort in reading order (left-to-right, top-to-bottom)
    boxes = sort_boxes_reading_order(boxes)

    return boxes
```

---

### 5.4.3 CNN Model Architecture

**File**: `backend/app/ml/model.py`

The heart of VattalettuX is the CNN model that classifies each character image. We designed a ResNet-inspired architecture called `VatteluttuCNN`.

**Building Blocks**

We defined two reusable building blocks:

```python
class ConvBlock(nn.Module):
    """Convolutional block with BatchNorm and ReLU."""
    def __init__(self, in_channels, out_channels,
                 kernel_size=3, stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels, out_channels,
            kernel_size, stride, padding, bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
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
        out += residual  # Skip connection
        return self.relu(out)
```

The `ConvBlock` is a standard convolution followed by batch normalization and ReLU activation. The `ResidualBlock` adds a **skip connection** — the input is added directly to the output of two convolution layers. This skip connection, borrowed from the ResNet architecture [17], helps the model train more effectively by allowing gradients to flow directly through the network during backpropagation.

**Main VatteluttuCNN Architecture**

```python
class VatteluttuCNN(nn.Module):
    """CNN classifier for Vatteluttu character recognition.

    Architecture:
    - Initial conv block: 1 -> 32 channels
    - 4 stages with increasing channels (32 -> 64 -> 128 -> 256 -> 512)
    - Each stage has conv + residual block + max pool
    - Global average pooling
    - Fully connected classifier

    Input: (batch, 1, 64, 64)
    Output: (batch, 247)
    """

    def __init__(self, num_classes=247, dropout=0.5):
        super().__init__()
        self.initial = ConvBlock(1, 32)

        # Stage 1: 32 -> 64, 64x64 -> 32x32
        self.stage1 = nn.Sequential(
            ConvBlock(32, 64), ResidualBlock(64), nn.MaxPool2d(2, 2))

        # Stage 2: 64 -> 128, 32x32 -> 16x16
        self.stage2 = nn.Sequential(
            ConvBlock(64, 128), ResidualBlock(128), nn.MaxPool2d(2, 2))

        # Stage 3: 128 -> 256, 16x16 -> 8x8
        self.stage3 = nn.Sequential(
            ConvBlock(128, 256), ResidualBlock(256), nn.MaxPool2d(2, 2))

        # Stage 4: 256 -> 512, 8x8 -> 4x4
        self.stage4 = nn.Sequential(
            ConvBlock(256, 512), ResidualBlock(512), nn.MaxPool2d(2, 2))

        self.global_pool = nn.AdaptiveAvgPool2d(1)

        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout * 0.5),
            nn.Linear(256, num_classes)
        )
```

The model processes a 64×64 grayscale input through four progressive stages. Each stage doubles the number of feature channels while halving the spatial dimensions through max pooling. By Stage 4, the model has extracted 512 high-level feature channels from a 4×4 spatial grid. Global average pooling collapses this to a single 512-element vector, which is then classified into one of 247 character classes by the fully connected layers.

**Feature Map Progression:**

| Layer | Channels | Spatial Size | Feature Maps |
|-------|----------|-------------|-------------|
| Input | 1 | 64 × 64 | Raw grayscale |
| Initial Conv | 32 | 64 × 64 | Low-level edges |
| Stage 1 | 64 | 32 × 32 | Stroke patterns |
| Stage 2 | 128 | 16 × 16 | Character components |
| Stage 3 | 256 | 8 × 8 | High-level features |
| Stage 4 | 512 | 4 × 4 | Abstract representations |
| Global Pool | 512 | 1 × 1 | Feature vector |
| Classifier | 247 | — | Class probabilities |

**Weight Initialization**: All convolution layers use He (Kaiming) initialization, which is the recommended initialization strategy for networks using ReLU activations.

**Dropout**: We apply 50% dropout before the first fully connected layer and 25% before the second. This prevents overfitting by randomly deactivating neurons during training, forcing the model to learn more robust features.

---

### 5.4.4 Model Training Pipeline

**Files**: `training/train.py`, `training/generate_data.py`, `training/dataset.py`

**Synthetic Data Generation**

Since no large public dataset of Vatteluttu characters exists, we created our own synthetic dataset using authentic Vatteluttu font resources. The `generate_data.py` script renders each of the 247 characters and applies realistic augmentations:

- **Rotation**: ±15° to simulate different carving angles
- **Shearing**: Horizontal and vertical shear to simulate perspective distortion
- **Stroke Variation**: Erosion and dilation to mimic different carving depths
- **Gaussian Noise**: Random pixel noise to simulate stone surface granularity
- **Salt-and-Pepper Noise**: Isolated dark and light spots
- **Textured Background**: Stone-like texture overlaid on the background

Each character was rendered 1,000 times with random combinations of these augmentations, resulting in a total dataset of **247,000 images** (247 classes × 1,000 images each).

The dataset was split as follows:
- **Training**: 70% (172,900 images)
- **Validation**: 15% (37,050 images)
- **Testing**: 15% (37,050 images)

**Training Configuration**

```python
# Training hyperparameters
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', patience=10, factor=0.5
)
```

| Parameter | Value | Explanation |
|-----------|-------|------------|
| Optimizer | Adam | Adaptive learning rate optimizer |
| Learning Rate | 0.001 | Starting learning rate |
| Loss Function | Cross-Entropy | Standard for multi-class classification |
| Batch Size | 32 | Number of images processed per gradient update |
| Epochs | 100 | Total training passes through the dataset |
| LR Scheduler | ReduceLROnPlateau | Halves LR if loss doesn't improve for 10 epochs |
| Dropout | 0.5 | Regularization to prevent overfitting |

---

### 5.4.5 Character Mapping Module

**Files**: `backend/app/ml/mapping.py`, `backend/app/core/label_to_char.json`

After the CNN predicts a character class (e.g., `va_037`), this module looks up the corresponding Modern Tamil character. The mapping data is stored in a JSON file:

```json
{
    "va_001": "அ",
    "va_002": "ஆ",
    "va_003": "இ",
    "va_004": "ஈ",
    "va_037": "க",
    ...
}
```

The mapping covers all 247 Vatteluttu characters organized into five categories:
- **Vowels (உயிர் எழுத்து)**: 12 characters (va_001 to va_012)
- **Aytham (ஆய்தம்)**: 1 character (va_013)
- **Pure Consonants (மெய் எழுத்து)**: 18 characters
- **Consonants**: 18 characters
- **Compound Characters (உயிர்மெய்)**: 198 characters

---

### 5.4.6 OCR Pipeline Orchestration

**File**: `backend/app/ocr/pipeline.py`

This module ties together all the preceding modules into a single end-to-end pipeline. When a user uploads an image, this is the function that runs the entire OCR process:

1. Load the image from uploaded bytes
2. Run the preprocessing pipeline (grayscale → denoise → binarize → morphology)
3. Run character segmentation (connected components → filtering → sorting)
4. For each segmented character: crop, resize to 64×64, classify with CNN
5. Map each prediction to Modern Tamil
6. Generate a traced image with visual annotations
7. Return the complete result

The pipeline returns a structured result containing:
- The combined Modern Tamil text
- A list of per-character details (label, Tamil character, confidence, bounding box)
- The path to the annotated traced image

---

### 5.4.7 FastAPI Backend

**Files**: `backend/app/main.py`, `backend/app/api/routes.py`, `backend/app/api/schemas.py`

**Application Initialization**

The FastAPI application is initialized with CORS middleware (to allow the React frontend to communicate with it), static file serving for media, and lifecycle event handlers:

```python
app = FastAPI(
    title="VatteluttuX OCR API",
    description="API for recognizing Vatteluttu Tamil inscriptions",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Key API Endpoints**

The recognition endpoint accepts a multipart file upload, processes it through the OCR pipeline, saves the result to the database, and returns a structured JSON response:

```python
@router.post("/recognize")
async def recognize_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Recognize Vatteluttu characters in an uploaded image."""
    # Read image bytes
    image_bytes = await image.read()

    # Run OCR pipeline
    result = pipeline.process_image(image_bytes)

    # Save to database
    crud.create_recognition(db, {
        "original_filename": image.filename,
        "recognized_text": result.raw_labels,
        "modern_text": result.tamil_text,
        "num_characters": result.num_characters,
        "avg_confidence": result.avg_confidence,
    })

    return result
```

**Pydantic Response Schemas**

All API responses are validated using Pydantic schemas, which ensure type safety and automatic documentation:

```python
class CharacterResult(BaseModel):
    label: str           # e.g., "va_037"
    tamil_char: str      # e.g., "க"
    confidence: float    # e.g., 0.94
    bounding_box: List[int]  # [x, y, width, height]
```

---

### 5.4.8 MySQL Database Integration

**Files**: `backend/app/db/database.py`, `backend/app/db/models.py`, `backend/app/db/crud.py`

**Database Connection**

The database connection is configured using SQLAlchemy ORM with PyMySQL as the MySQL driver:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:@localhost/vattalettux"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**Database Model**

The `RecognitionHistory` model maps directly to a MySQL table:

```python
class RecognitionHistory(Base):
    __tablename__ = "recognition_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_filename = Column(String(255), nullable=False)
    recognized_text = Column(Text, nullable=False)
    modern_text = Column(Text, nullable=False)
    num_characters = Column(Integer, default=0)
    num_words = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)
    traced_image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

This table is automatically created when the application starts, and it can be browsed and managed through phpMyAdmin at `http://localhost/phpmyadmin`.

**CRUD Operations**

The `crud.py` file provides functions for creating, reading, and deleting history records:

```python
def create_recognition(db: Session, data: dict):
    """Save a new recognition result to the database."""
    record = RecognitionHistory(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_recognitions(db: Session, skip=0, limit=50):
    """Get recognition history (newest first)."""
    return db.query(RecognitionHistory) \
        .order_by(RecognitionHistory.created_at.desc()) \
        .offset(skip).limit(limit).all()
```

---

### 5.4.9 React.js Frontend

**Directory**: `frontend/src/components/`

The frontend is built using React.js 19.2 with TypeScript and Vite as the build tool. It consists of seven main components:

**1. UploadPanel Component** (`UploadPanel.tsx`)
This component provides a drag-and-drop area for uploading inscription images. It handles file validation (checking that the uploaded file is an image of acceptable size) and triggers the API call to the backend's `/recognize` endpoint.

**2. RecognitionPage Component** (`RecognitionPage.tsx`)
The main page that contains the UploadPanel and ResultsDisplay. It manages the overall recognition workflow state — idle, uploading, processing, and results.

**3. ResultsDisplay Component** (`ResultsDisplay.tsx`)
Displays the OCR results after processing. It shows:
- The traced image with colored bounding boxes around each detected character
- Individual character chips with their Modern Tamil equivalents
- Confidence percentages for each prediction
- The combined Modern Tamil text output

**4. HistoryPage Component** (`HistoryPage.tsx`)
Fetches and displays past recognition sessions from the MySQL database via the `/history` API endpoint. Each record shows the filename, recognized text, number of characters, and timestamp. Users can delete individual records.

**5. CharacterMappingViewer Component** (`CharacterMappingViewer.tsx`)
Displays the complete 247-character mapping table. Includes category filtering (vowels, consonants, compounds, etc.) and search functionality.

**6. CharacterTable Component** (`CharacterTable.tsx`)
A reusable table component that renders character mapping data in a structured grid format.

**7. Header Component** (`Header.tsx`)
The navigation bar that appears on all pages, containing the application title and links to the Recognition, History, and Character Map pages.

**API Communication**

The frontend communicates with the backend using the Fetch API. API utility functions are defined in `frontend/src/utils/api.ts`:

```typescript
const API_BASE = "http://localhost:8000";

export async function recognizeImage(file: File) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE}/recognize`, {
        method: "POST",
        body: formData,
    });

    return await response.json();
}
```

---

## 5.5 Challenges Faced During Implementation

| # | Challenge | How We Solved It |
|---|-----------|-----------------|
| 1 | **No public dataset** of labeled Vatteluttu characters | Created a synthetic dataset of 247,000 images with realistic augmentations |
| 2 | **Broken character strokes** on worn stone surfaces | Applied morphological closing before segmentation to reconnect broken strokes |
| 3 | **Similar-looking characters** among the 198 compound (Uyirmei) characters | Used a deeper CNN with residual connections and 50% dropout to improve discrimination |
| 4 | **Varying image polarity** — some images have dark text on light stone, others light on dark | Added `ensure_white_on_black()` function that automatically detects and normalizes polarity |
| 5 | **Merged characters** in closely packed inscriptions | Implemented `split_wide_boxes()` using vertical projection profile analysis to split merged characters |
| 6 | **Noise from stone texture** appearing as false character detections | Multi-stage filtering: solidity check, median size filter, and aspect ratio constraints |
| 7 | **Database not starting** when XAMPP MySQL is not running | Added graceful error handling with clear error messages guiding the user to start MySQL |

---
