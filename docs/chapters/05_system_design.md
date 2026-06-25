# CHAPTER 4: SYSTEM DESIGN

---

## 4.1 Introduction

System design translates the requirements identified in the previous chapter into a detailed technical blueprint for the system. This chapter describes the overall architecture, data flow design, database design, individual module design, API specifications, and user interface design of VattalettuX. The design follows a modular approach, where each component of the system has a clearly defined responsibility and interacts with other components through well-defined interfaces.

---

## 4.2 System Architecture

VattalettuX follows a **client-server architecture** with a clear separation between the frontend (user interface) and the backend (processing engine). The communication between the frontend and backend happens through RESTful API calls over HTTP.

### 4.2.1 Architectural Pattern: Client-Server

The client-server pattern divides the system into two main parts:

- **Client (Frontend)**: The part of the application that runs in the user's web browser. It is responsible for presenting the user interface, collecting user input (the uploaded image), and displaying the results returned by the server. The client is built with React.js and TypeScript, compiled by Vite, and served as static HTML/CSS/JavaScript files.

- **Server (Backend)**: The part of the application that runs on the server machine. It handles all the heavy processing — receiving uploaded images, running the OCR pipeline (preprocessing, segmentation, classification, mapping), interacting with the MySQL database, and returning structured JSON responses to the client. The server is built with Python using the FastAPI framework and runs on the Uvicorn ASGI server.

This separation provides several important benefits:

1. **Independence**: The frontend and backend can be developed, tested, and deployed independently. Changes to the UI do not require changes to the backend, and vice versa.
2. **Scalability**: The backend server can be deployed on a more powerful machine (or cloud server) while the frontend runs in the user's browser on any device.
3. **Reusability**: The same backend API can serve multiple clients — a web browser today, a mobile app in the future.
4. **Security**: The ML model and database are on the server side, not exposed directly to the user.

### 4.2.2 Communication Protocol: REST API

The frontend and backend communicate using **REST (Representational State Transfer)** over HTTP. REST is the most widely used architectural style for web APIs. In REST:

- Each URL represents a **resource** (e.g., `/recognize` for recognition, `/history` for history records).
- Standard HTTP methods are used: **GET** to retrieve data, **POST** to submit data, **DELETE** to remove data.
- Data is exchanged in **JSON format**, which is lightweight and easy to parse in both Python and JavaScript/TypeScript.
- Each request is **stateless** — the server does not maintain session state between requests. All information needed to process a request is included in the request itself.

### 4.2.3 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT SIDE                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   React.js + TypeScript Frontend              │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐    │  │
│  │  │  Upload   │  │  Recognition │  │  Character Mapping   │    │  │
│  │  │  Panel    │  │  Page        │  │  Viewer              │    │  │
│  │  └──────────┘  └──────────────┘  └──────────────────────┘    │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐    │  │
│  │  │ Results  │  │   History    │  │     Header /          │    │  │
│  │  │ Display  │  │   Page       │  │     Navigation        │    │  │
│  │  └──────────┘  └──────────────┘  └──────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │  HTTP / REST API
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           SERVER SIDE                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Backend (Python)                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │                   API Router (routes.py)                │  │  │
│  │  │  /recognize  /history  /characters  /health  /labels    │  │  │
│  │  └──────────────────────────┬──────────────────────────────┘  │  │
│  │                             │                                 │  │
│  │  ┌──────────────────────────▼──────────────────────────────┐  │  │
│  │  │              OCR Processing Pipeline                    │  │  │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │  │  │
│  │  │  │ Preprocess│→│ Segment  │→│ Classify │→│  Mapping  │  │  │  │
│  │  │  │ (OpenCV)  │ │  (CCA)   │ │  (CNN)   │ │  (JSON)   │  │  │  │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                             │                                 │  │
│  │  ┌──────────────────────────▼──────────────────────────────┐  │  │
│  │  │                   Storage Layer                         │  │  │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐    │  │  │
│  │  │  │  MySQL   │ │  Model   │ │  Media / Uploads     │    │  │  │
│  │  │  │ Database │ │  Weights │ │  (Images)            │    │  │  │
│  │  │  └──────────┘ └──────────┘ └──────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

*Figure 4.1: System Architecture Diagram of VattalettuX*

### Architecture Components

| Component | Technology | Responsibility |
|-----------|-----------|---------------|
| Frontend | React.js 19.2, TypeScript 5.9, Vite 7.2 | User interface, image upload, results display, navigation |
| Backend | Python 3.10+, FastAPI 0.109 | API endpoints, request handling, business logic |
| OCR Engine | PyTorch 2.1, OpenCV 4.9 | Image preprocessing, segmentation, CNN classification |
| Database | MySQL 8.0, SQLAlchemy 2.0 | Recognition history storage and retrieval |
| Media Storage | File system | Uploaded images and traced output images |
| Model Storage | File system (.pth file) | Trained CNN model weights |

---

## 4.3 Data Flow Diagrams

Data Flow Diagrams (DFDs) show how data moves through the system at different levels of detail.

### 4.3.1 DFD Level 0 (Context Diagram)

The Level 0 DFD shows the system as a single process interacting with external entities.

```
                    ┌─────────────────────┐
                    │                     │
   Inscription  ──→ │    VattalettuX      │ ──→  Modern Tamil Text
   Image            │      System         │ ──→  Confidence Scores
                    │                     │ ──→  Annotated Image
   History      ──→ │                     │ ──→  History Records
   Request          │                     │
                    └─────────────────────┘
                              ▲
                              │
                     ┌────────┴────────┐
                     │  User /         │
                     │  Researcher     │
                     └─────────────────┘
```

*Figure 4.2: DFD Level 0 — Context Diagram*

### 4.3.2 DFD Level 1

The Level 1 DFD breaks the system into its major processes.

```
┌──────────┐     Image        ┌────────────────┐    Cleaned       ┌────────────────┐
│          │ ──────────────→  │   1.0 Image     │    Image     ──→│  2.0 Character  │
│  User /  │                  │  Preprocessing  │                  │  Segmentation   │
│Researcher│                  └────────────────┘                  └────────┬───────┘
│          │                                                               │
│          │                                                     Character Chips
│          │                                                               │
│          │                                                               ▼
│          │                  ┌────────────────┐                  ┌────────────────┐
│          │  Tamil Text   ←──│   4.0 Tamil     │  Class Labels ←──│  3.0 CNN       │
│          │  + Confidence    │   Mapping       │                  │  Recognition    │
│          │                  └───────┬────────┘                  └────────────────┘
│          │                          │                                    │
│          │                    ┌─────▼──────┐                    ┌───────▼────────┐
│          │  History        ←──│ Character   │                   │  Model Weights │
│          │  Records           │ Map (JSON)  │                   │    (.pth)      │
│          │                    └─────────────┘                   └────────────────┘
│          │
│          │  History Request  ┌────────────────┐                 ┌────────────────┐
│          │ ──────────────→  │  5.0 History    │ ──── CRUD ───→  │   MySQL        │
│          │  History Data  ←──│   Management   │ ← ─ ─ ─ ─ ─ ──│   Database     │
└──────────┘                  └────────────────┘                  └────────────────┘
```

*Figure 4.3: DFD Level 1*

### 4.3.3 DFD Level 2 — Image Preprocessing (Process 1.0)

```
                    ┌─────────────────┐
   Raw Image   ──→  │  1.1 Grayscale   │
                    │   Conversion     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  1.2 Adaptive    │
                    │  Thresholding    │
                    │  (Binarization)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  1.3 Morphological│
                    │  Opening (Noise  │
                    │  Removal)        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  1.4 Histogram   │ ──→  Cleaned Image
                    │  Equalization    │
                    └─────────────────┘
```

*Figure 4.4: DFD Level 2 — Image Preprocessing Sub-processes*

### 4.3.4 DFD Level 2 — Character Segmentation (Process 2.0)

```
                    ┌─────────────────┐
  Cleaned Image ──→ │  2.1 Connected   │
                    │  Component       │
                    │  Labeling        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  2.2 Bounding    │
                    │  Box Extraction  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  2.3 Size/Shape  │
                    │  Filtering       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  2.4 Crop &      │ ──→  64×64 Character Chips
                    │  Resize to 64×64 │
                    └─────────────────┘
```

*Figure 4.5: DFD Level 2 — Character Segmentation Sub-processes*

---

## 4.4 Entity-Relationship Diagram

The ER diagram shows the database entities and their relationships.

```
  ┌─────────────────────────┐          ┌─────────────────────────┐
  │   RECOGNITION_HISTORY   │          │     CHARACTER_MAP       │
  ├─────────────────────────┤          ├─────────────────────────┤
  │  id (PK, INT, AUTO)     │          │  label_id (PK, VARCHAR) │
  │  original_filename      │          │  modern_tamil_char      │
  │  image_path             │          │  unicode_point          │
  │  traced_image_path      │          │  category               │
  │  recognized_text        │          │  phonetics              │
  │  num_characters         │          └─────────────────────────┘
  │  confidence_avg         │
  │  characters_json        │
  │  created_at             │
  └─────────────────────────┘
```

*Figure 4.6: Entity-Relationship Diagram*

### Relationship Description

The current system uses two main data entities:

1. **RECOGNITION_HISTORY**: Stores the details of each OCR recognition session — the input image, output text, number of characters detected, average confidence score, and a JSON blob containing per-character details (bounding boxes, individual predictions, confidence scores).

2. **CHARACTER_MAP**: Stores the mapping of each of the 247 Vatteluttu character labels to their Modern Tamil equivalents. This is loaded from a JSON file at startup and used for the mapping step.

In the current design, these entities are logically related (the `characters_json` field in `RECOGNITION_HISTORY` contains `label_id` values that correspond to entries in `CHARACTER_MAP`), but they are not formally linked by a foreign key constraint. This is a deliberate design choice to keep the recognition history self-contained — each history record stores a complete snapshot of the recognition results.

---

## 4.5 Database Design

### 4.5.1 Table: recognition_history

| Column | Data Type | Constraints | Description |
|--------|-----------|------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique record identifier |
| `original_filename` | VARCHAR(255) | NOT NULL | Name of the uploaded image file |
| `image_path` | VARCHAR(500) | NOT NULL | Server path to the saved uploaded image |
| `traced_image_path` | VARCHAR(500) | NULLABLE | Server path to the annotated output image |
| `recognized_text` | TEXT | NOT NULL | The combined Modern Tamil text output |
| `num_characters` | INT | NOT NULL, DEFAULT 0 | Number of characters detected |
| `confidence_avg` | FLOAT | NULLABLE | Average confidence score across all predictions |
| `characters_json` | JSON | NULLABLE | Full per-character details (label, Tamil char, confidence, bounding box) |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp of the recognition |

### 4.5.2 Table: character_map (Conceptual)

| Column | Data Type | Constraints | Description |
|--------|-----------|------------|-------------|
| `label_id` | VARCHAR(10) | PRIMARY KEY | Internal model class label (e.g., `va_037`) |
| `modern_tamil_char` | NVARCHAR(5) | NOT NULL | Modern Tamil Unicode character |
| `unicode_point` | VARCHAR(10) | NOT NULL | Unicode code point (e.g., `U+0B95`) |
| `category` | VARCHAR(20) | NOT NULL | Linguistic category (vowel, consonant, etc.) |
| `phonetics` | VARCHAR(50) | NULLABLE | Phonetic description |

> **Note**: The character map is currently stored as a JSON file (`label_to_char.json`) loaded at application startup. The table above represents its logical structure.

---

## 4.6 Module Design

VattalettuX is divided into the following modules, each with a specific responsibility:

### Module 1: Image Preprocessing Module

| Attribute | Details |
|-----------|---------|
| **File** | `backend/app/ml/preprocessing.py` |
| **Purpose** | Clean and enhance raw inscription images for character detection |
| **Input** | Raw image file (JPEG, PNG, BMP, TIFF) |
| **Output** | Cleaned binary image ready for segmentation |
| **Key Functions** | `preprocess_image()`, `apply_adaptive_threshold()`, `morphological_clean()`, `enhance_contrast()` |
| **Dependencies** | OpenCV, NumPy |

### Module 2: Character Segmentation Module

| Attribute | Details |
|-----------|---------|
| **File** | `backend/app/ocr/segmentation.py` |
| **Purpose** | Detect and extract individual characters from a preprocessed image |
| **Input** | Cleaned binary image |
| **Output** | List of 64×64 pixel character images with bounding box coordinates |
| **Key Functions** | `segment_characters()`, `find_connected_components()`, `filter_by_size()`, `crop_and_resize()` |
| **Dependencies** | OpenCV, NumPy |

### Module 3: CNN Classification Module

| Attribute | Details |
|-----------|---------|
| **Files** | `backend/app/ml/model.py`, `backend/app/ml/inference.py` |
| **Purpose** | Classify each 64×64 character image into one of 247 Vatteluttu classes |
| **Input** | 64×64 grayscale character image |
| **Output** | Predicted class label and confidence score |
| **Key Classes** | `VatteluttuNet` (model architecture), `VatteluttuInference` (inference wrapper) |
| **Dependencies** | PyTorch, TorchVision |

### Module 4: Character Mapping Module

| Attribute | Details |
|-----------|---------|
| **File** | `backend/app/ml/mapping.py`, `backend/app/core/label_to_char.json` |
| **Purpose** | Convert predicted class labels to Modern Tamil Unicode characters |
| **Input** | Class label string (e.g., `va_037`) |
| **Output** | Modern Tamil character (e.g., `க`) |
| **Key Functions** | `labels_to_tamil()`, `get_character_info()`, `get_category_labels()` |
| **Dependencies** | JSON, Python standard library |

### Module 5: OCR Pipeline Module

| Attribute | Details |
|-----------|---------|
| **File** | `backend/app/ocr/pipeline.py` |
| **Purpose** | Orchestrate the entire OCR workflow — preprocessing → segmentation → classification → mapping |
| **Input** | Raw image file |
| **Output** | Complete recognition result with text, characters, confidence, and traced image |
| **Key Functions** | `run_pipeline()`, `process_image()` |
| **Dependencies** | Modules 1–4 |

### Module 6: API Module

| Attribute | Details |
|-----------|---------|
| **Files** | `backend/app/api/routes.py`, `backend/app/api/schemas.py` |
| **Purpose** | Expose REST API endpoints for the frontend to interact with |
| **Endpoints** | `/recognize`, `/history`, `/characters`, `/character-map`, `/health`, `/labels` |
| **Key Schemas** | `RecognitionResponse`, `HistoryResponse`, `CharacterInfo` |
| **Dependencies** | FastAPI, Pydantic |

### Module 7: Database Module

| Attribute | Details |
|-----------|---------|
| **Files** | `backend/app/db/database.py`, `backend/app/db/models.py`, `backend/app/db/crud.py` |
| **Purpose** | Handle all database operations — connection, table creation, CRUD operations |
| **Key Functions** | `init_db()`, `get_db()`, `create_recognition()`, `get_recognitions()`, `delete_recognition()` |
| **Dependencies** | SQLAlchemy, PyMySQL, MySQL |

### Module 8: Frontend Module

| Attribute | Details |
|-----------|---------|
| **Directory** | `frontend/src/components/` |
| **Purpose** | Provide the user interface for all system interactions |
| **Components** | `UploadPanel`, `RecognitionPage`, `ResultsDisplay`, `HistoryPage`, `CharacterMappingViewer`, `CharacterTable`, `Header` |
| **Dependencies** | React.js, TypeScript, Vite |

### Module 9: Training Module

| Attribute | Details |
|-----------|---------|
| **Directory** | `training/` |
| **Purpose** | Train the CNN model on the synthetic Vatteluttu character dataset |
| **Files** | `generate_data.py` (data generation), `dataset.py` (PyTorch dataset), `train.py` (training loop) |
| **Dependencies** | PyTorch, TorchVision, PIL, OpenCV |

---

## 4.7 Sequence Diagram

The following sequence diagram shows the flow of events when a user uploads an inscription image for recognition:

```
User          Frontend         API Server       OCR Pipeline      Database
 │               │                 │                 │                │
 │  Upload Image │                 │                 │                │
 │──────────────→│                 │                 │                │
 │               │  POST /recognize│                 │                │
 │               │────────────────→│                 │                │
 │               │                 │  Run Pipeline   │                │
 │               │                 │────────────────→│                │
 │               │                 │                 │                │
 │               │                 │   Preprocess    │                │
 │               │                 │   Image         │                │
 │               │                 │                 │                │
 │               │                 │   Segment       │                │
 │               │                 │   Characters    │                │
 │               │                 │                 │                │
 │               │                 │   Classify      │                │
 │               │                 │   (CNN Model)   │                │
 │               │                 │                 │                │
 │               │                 │   Map to Tamil  │                │
 │               │                 │                 │                │
 │               │                 │   Generate      │                │
 │               │                 │   Traced Image  │                │
 │               │                 │                 │                │
 │               │                 │  Return Results │                │
 │               │                 │←────────────────│                │
 │               │                 │                 │                │
 │               │                 │  Save to History│                │
 │               │                 │────────────────────────────────→│
 │               │                 │                 │                │
 │               │  JSON Response  │                 │                │
 │               │←────────────────│                 │                │
 │               │                 │                 │                │
 │  Show Results │                 │                 │                │
 │←──────────────│                 │                 │                │
 │               │                 │                 │                │
```

*Figure 4.7: Sequence Diagram — Image Recognition Flow*

---

## 4.8 API Endpoint Design

The following table describes all REST API endpoints provided by the VattalettuX backend:

| # | Method | Endpoint | Description | Request | Response |
|---|--------|----------|-------------|---------|----------|
| 1 | GET | `/` | Root endpoint — API information | — | JSON with API name and version |
| 2 | GET | `/health` | Health check — server and model status | — | JSON with status, model loaded flag, num_classes |
| 3 | POST | `/recognize` | Upload image for OCR recognition | Multipart file upload | JSON with recognized text, characters, traced image path |
| 4 | GET | `/history` | Retrieve recognition history list | Query params: skip, limit | JSON array of history records |
| 5 | GET | `/history/{id}` | Get a single history record | Path param: record_id | JSON with full recognition details |
| 6 | DELETE | `/history/{id}` | Delete a history record | Path param: record_id | Confirmation message |
| 7 | GET | `/labels` | Get all character labels | — | JSON with label-to-char mappings |
| 8 | GET | `/labels/{label}` | Get info for a specific label | Path param: label string | JSON with label details |
| 9 | GET | `/characters` | Get all characters (with optional filter) | Query param: category | JSON array of character objects |
| 10 | GET | `/character-map` | Get full character map with stats | — | JSON with complete mapping and category counts |

---

## 4.9 User Interface Design

The VattalettuX frontend consists of four main pages, each served by a dedicated React component:

### Page 1: Recognition Page (Home)

This is the primary page of the application. It contains:
- A drag-and-drop upload area where users can drop an inscription image
- A preview of the uploaded image
- After processing: the traced image with colored bounding boxes showing detected characters
- A results panel showing each character chip alongside its Modern Tamil equivalent and confidence score
- The combined Modern Tamil text output

### Page 2: History Page

This page displays all past recognition sessions:
- A list of records sorted by date (newest first)
- Each record shows the filename, recognized text, number of characters, and timestamp
- A delete button to remove individual records
- A "No history" message when the database is empty

### Page 3: Character Mapping Viewer

This page displays the complete 247-character mapping:
- A search/filter bar to search for specific characters
- Category filter buttons (All, Vowels, Consonants, Compounds, etc.)
- A grid or table showing each label code, the Modern Tamil character, and the category
- Color-coded categories for visual clarity

### Page 4: Header / Navigation

A persistent navigation header across all pages:
- Application logo and title
- Navigation links to Recognition, History, and Character Map pages
- Visual indicator for the currently active page

*Note: Screenshots of the actual running application are included in Chapter 6 (Testing & Results) and Appendix C.*

---
