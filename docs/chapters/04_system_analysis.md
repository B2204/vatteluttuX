# CHAPTER 3: SYSTEM ANALYSIS

---

## 3.1 Introduction

System analysis is the process of studying an existing situation, understanding its problems, and defining the requirements for a new system that can solve those problems. In this chapter, we first look at how Vatteluttu inscriptions are currently read (the existing system), then describe the proposed VattalettuX system, conduct a feasibility study, and finally define the detailed functional and non-functional requirements of the system.

---

## 3.2 Existing System

The existing approach to reading Vatteluttu inscriptions is entirely manual and depends on a very small number of trained human experts called epigraphists. The process typically works as follows:

1. **Field Survey**: An archaeologist or field researcher visits a heritage site and photographs the stone inscription.
2. **Expert Review**: The photographs (or sometimes hand-drawn copies called "estampages") are sent to an epigraphist who can read Vatteluttu script.
3. **Manual Decipherment**: The epigraphist examines each character in the inscription, identifies it, and writes down the corresponding Modern Tamil letter. This step requires deep knowledge of the script, its historical variations, and the conventions used by different dynasties.
4. **Verification**: The transliteration is reviewed and verified by the epigraphist or a colleague.
5. **Publication**: The final reading is published in an academic journal, government report, or inscription catalogue.

### Limitations of the Existing System

| # | Limitation | Description |
|---|-----------|-------------|
| 1 | **Speed** | A single inscription can take hours or days to decipher manually, depending on its length and the condition of the stone surface. |
| 2 | **Scalability** | There are only a handful of epigraphists in India who can read Vatteluttu. Thousands of catalogued inscriptions remain unread simply because there are not enough experts. |
| 3 | **Human Error** | Manual reading is subjective and prone to inconsistencies. Different experts may interpret damaged or ambiguous characters differently. |
| 4 | **No Digital Record** | The manual process typically produces a paper-based record. There is no structured digital database of readings that can be searched, queried, or analyzed computationally. |
| 5 | **Accessibility** | Only people with specialized training can participate. The general public, students, and even most historians cannot read Vatteluttu themselves. |
| 6 | **Knowledge Loss Risk** | As the current generation of epigraphists retires, their expertise is at risk of being lost forever, since there are very few younger scholars being trained in this skill. |

---

## 3.3 Proposed System

VattalettuX is an automated OCR system that replaces the manual decipherment process with a four-stage computer pipeline. The system accepts a photograph of a Vatteluttu inscription as input and produces the corresponding Modern Tamil text as output — all within a few seconds.

### Key Features of the Proposed System

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Automated Recognition** | Uses a deep learning CNN model to automatically classify 247 Vatteluttu characters without human intervention. |
| 2 | **Image Preprocessing** | Automatically cleans and enhances inscription photographs to handle noise, shadows, and surface damage. |
| 3 | **Character Segmentation** | Detects and isolates individual characters from the inscription image using Connected Component Analysis. |
| 4 | **Modern Tamil Output** | Maps each recognized Vatteluttu character to its equivalent Modern Tamil Unicode character. |
| 5 | **Web-Based Interface** | Provides a browser-based application where users can upload images and view results without installing any software. |
| 6 | **Recognition History** | Stores all recognition sessions in a MySQL database for future reference and review. |
| 7 | **Character Map Viewer** | Displays the complete mapping of all 247 Vatteluttu characters to their Modern Tamil equivalents. |
| 8 | **Visual Feedback** | Shows bounding boxes around detected characters on the original image and displays confidence scores for each prediction. |

### Advantages Over the Existing System

- **Speed**: Processes an image in approximately 1.8 seconds (compared to hours of manual work).
- **Scalability**: Can process unlimited inscriptions simultaneously when hosted on a server.
- **Consistency**: The same image will always produce the same output — no subjective variation.
- **Accessibility**: Anyone with a web browser can use the system, regardless of expertise.
- **Digital Records**: All results are stored in a structured database that can be searched and analyzed.

---

## 3.4 Feasibility Study

Before developing any system, it is important to assess whether the project is feasible from multiple perspectives. We evaluated VattalettuX across three dimensions:

### 3.4.1 Technical Feasibility

| Factor | Assessment |
|--------|-----------|
| **Deep Learning Frameworks** | Mature, well-documented frameworks (PyTorch, TorchVision) are freely available for building and training CNN models. |
| **Web Technologies** | FastAPI (Python) and React.js (JavaScript) are modern, production-ready frameworks for building web applications. |
| **Image Processing Libraries** | OpenCV and Pillow provide comprehensive image processing capabilities including thresholding, morphological operations, and component analysis. |
| **Training Data** | While no large public dataset exists, we can generate synthetic training data programmatically from authentic Vatteluttu font resources. |
| **Hardware** | The model can be trained on a machine with a standard GPU and deployed for inference on a standard CPU. |
| **Database** | MySQL is a well-established relational database that is free, reliable, and easy to manage with tools like phpMyAdmin. |

**Conclusion**: The project is technically feasible. All required technologies and tools are freely available and well-supported.

### 3.4.2 Operational Feasibility

| Factor | Assessment |
|--------|-----------|
| **Target Users** | Archaeologists, historians, students, and the general public — all of whom are comfortable using web browsers. |
| **User Interface** | The drag-and-drop interface requires no technical expertise. Users simply upload an image and receive the result. |
| **Training Required** | Minimal to none. The interface is self-explanatory with clear visual feedback. |
| **Maintenance** | The system is modular, allowing the AI model to be updated or improved without changing the rest of the application. |

**Conclusion**: The project is operationally feasible. The target users can use the system without specialized training.

### 3.4.3 Economic Feasibility

| Factor | Assessment |
|--------|-----------|
| **Development Cost** | All frameworks and libraries used are open-source and free. No commercial software licenses required. |
| **Hardware Cost** | Training requires a GPU-equipped machine (available for free on platforms like Google Colab). Deployment can run on a standard desktop or a cloud VM costing approximately $5-20/month. |
| **Maintenance Cost** | Minimal ongoing cost. The web application can run on a single server. |
| **Benefit** | The cultural and academic value of making thousands of inscriptions readable far outweighs the minimal development and hosting costs. |

**Conclusion**: The project is economically feasible with very low development and operational costs.

---

## 3.5 Functional Requirements

Functional requirements define what the system should do — the specific capabilities and features it must provide.

| ID | Requirement | Description | Priority |
|----|------------|-------------|----------|
| FR-01 | Image Upload | The system shall allow users to upload inscription images in common formats (JPEG, PNG, BMP, TIFF). | High |
| FR-02 | Image Preprocessing | The system shall automatically clean and enhance uploaded images using grayscale conversion, adaptive thresholding, morphological operations, and histogram equalization. | High |
| FR-03 | Character Segmentation | The system shall automatically detect and isolate individual characters from the preprocessed image using Connected Component Analysis. | High |
| FR-04 | Character Recognition | The system shall classify each segmented character into one of 247 Vatteluttu character classes using a trained CNN model. | High |
| FR-05 | Modern Tamil Mapping | The system shall convert each recognized character code into its corresponding Modern Tamil Unicode character. | High |
| FR-06 | Confidence Display | The system shall display a confidence score (0–100%) for each character prediction. | Medium |
| FR-07 | Bounding Box Visualization | The system shall draw colored bounding boxes around each detected character on the original image. | Medium |
| FR-08 | Traced Image | The system shall generate an annotated version of the input image showing character locations and predictions. | Medium |
| FR-09 | Recognition History | The system shall save each recognition session (image path, recognized text, timestamp) to a MySQL database. | High |
| FR-10 | History Retrieval | The system shall allow users to view, search, and browse past recognition sessions. | Medium |
| FR-11 | History Deletion | The system shall allow users to delete individual recognition history records. | Low |
| FR-12 | Character Map Viewer | The system shall display the complete mapping of all 247 Vatteluttu characters to Modern Tamil, organized by category. | Medium |
| FR-13 | Category Filtering | The system shall allow users to filter the character map by category (vowels, consonants, compounds, etc.). | Low |
| FR-14 | API Health Check | The system shall provide a health check endpoint to verify server status and model availability. | Medium |
| FR-15 | Error Handling | The system shall display clear, user-friendly error messages when image processing or recognition fails. | High |

---

## 3.6 Non-Functional Requirements

Non-functional requirements define the quality attributes and constraints of the system — how the system should perform.

| ID | Requirement | Description | Target |
|----|------------|-------------|--------|
| NFR-01 | Performance | Average end-to-end processing time per image (5–15 characters) | ≤ 3 seconds on CPU |
| NFR-02 | Accuracy | Top-1 classification accuracy on the test set | ≥ 90% |
| NFR-03 | Availability | System uptime when deployed | ≥ 99% (excluding planned maintenance) |
| NFR-04 | Usability | Time for a new user to successfully upload and process their first image | ≤ 2 minutes |
| NFR-05 | Scalability | Ability to handle multiple concurrent user requests | ≥ 10 concurrent users |
| NFR-06 | Security | Upload file validation to prevent malicious files | Validate file type and size |
| NFR-07 | Compatibility | Browser support | Chrome, Firefox, Edge, Safari (latest versions) |
| NFR-08 | Responsiveness | Frontend layout adaptation | Desktop and tablet screens |
| NFR-09 | Maintainability | Modular codebase allowing independent updates to any component | Clear separation of concerns |
| NFR-10 | Data Integrity | All database transactions must be atomic and consistent | ACID compliance via MySQL |

---

## 3.7 Hardware and Software Requirements

### 3.7.1 Hardware Requirements

**For Development and Training:**

| Component | Minimum Requirement |
|-----------|-------------------|
| Processor | Intel Core i5 (8th Gen) or equivalent |
| RAM | 8 GB |
| Storage | 10 GB free disk space (for dataset and models) |
| GPU | NVIDIA GPU with CUDA support (for training) |
| Display | 1920 × 1080 resolution |
| Network | Internet connection for package downloads |

**For Deployment (Server):**

| Component | Minimum Requirement |
|-----------|-------------------|
| Processor | Intel Core i3 or equivalent |
| RAM | 4 GB |
| Storage | 5 GB free disk space |
| GPU | Not required (CPU inference is supported) |
| Network | Internet connection for web access |

### 3.7.2 Software Requirements

**Backend:**

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Primary programming language |
| PyTorch | 2.1+ | Deep learning framework |
| TorchVision | 0.16+ | Image transforms and utilities |
| FastAPI | 0.109+ | REST API framework |
| Uvicorn | 0.27+ | ASGI server |
| OpenCV | 4.9+ | Image processing |
| Pillow | 10.0+ | Image I/O operations |
| NumPy | 1.26+ | Numerical computations |
| SQLAlchemy | 2.0+ | Database ORM |
| PyMySQL | 1.1+ | MySQL connector |
| Pydantic | 2.5+ | Data validation |

**Frontend:**

| Software | Version | Purpose |
|----------|---------|---------|
| Node.js | 18+ | JavaScript runtime |
| React.js | 19.2+ | UI component framework |
| TypeScript | 5.9+ | Type-safe JavaScript |
| Vite | 7.2+ | Build tool and dev server |

**Database:**

| Software | Version | Purpose |
|----------|---------|---------|
| MySQL | 8.0+ | Relational database |
| XAMPP | Latest | Local MySQL server and phpMyAdmin |

**Development Tools:**

| Software | Purpose |
|----------|---------|
| VS Code | Code editor |
| Git | Version control |
| Chrome / Firefox | Web browser for testing |
| phpMyAdmin | MySQL database management |

---

## 3.8 Use Case Diagram

The following use case diagram shows the primary interactions between the user (actor) and the VattalettuX system:

```
┌──────────────────────────────────────────────────────────────────┐
│                      VattalettuX System                          │
│                                                                  │
│   ┌──────────────────────┐     ┌──────────────────────────┐     │
│   │   Upload Inscription │     │  View Character Map      │     │
│   │       Image          │     │                          │     │
│   └──────────────────────┘     └──────────────────────────┘     │
│                                                                  │
│   ┌──────────────────────┐     ┌──────────────────────────┐     │
│   │   View Recognition   │     │  Filter Characters by    │     │
│   │      Results         │     │      Category            │     │
│   └──────────────────────┘     └──────────────────────────┘     │
│                                                                  │
│   ┌──────────────────────┐     ┌──────────────────────────┐     │
│   │   View Recognition   │     │   Delete History         │     │
│   │      History         │     │      Record              │     │
│   └──────────────────────┘     └──────────────────────────┘     │
│                                                                  │
│   ┌──────────────────────┐     ┌──────────────────────────┐     │
│   │   Download Traced    │     │   Check System Health    │     │
│   │      Image           │     │                          │     │
│   └──────────────────────┘     └──────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
       ▲
       │
   ┌───┴───┐
   │ User/ │
   │Resear-│
   │ cher  │
   └───────┘
```

*Figure 3.1: Use Case Diagram for VattalettuX System*

---

## 3.9 Use Case Descriptions

### Use Case 1: Upload Inscription Image

| Field | Description |
|-------|------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Upload Inscription Image |
| **Actor** | User / Researcher |
| **Description** | The user uploads a photograph of a Vatteluttu stone inscription to the system for recognition. |
| **Preconditions** | The system is running and accessible via web browser. The user has an inscription image file. |
| **Main Flow** | 1. User navigates to the recognition page. 2. User drags and drops an image file (or clicks to browse). 3. System validates the file type and size. 4. System displays a preview of the uploaded image. 5. System begins automatic OCR processing. |
| **Postconditions** | The image is uploaded and OCR processing begins. Results are displayed when ready. |
| **Alternative Flow** | If the file type is invalid, the system shows an error message asking the user to upload a supported format. |

### Use Case 2: View Recognition Results

| Field | Description |
|-------|------------|
| **Use Case ID** | UC-02 |
| **Use Case Name** | View Recognition Results |
| **Actor** | User / Researcher |
| **Description** | After uploading an image, the user views the recognition results including identified characters, Modern Tamil text, confidence scores, and annotated image. |
| **Preconditions** | An image has been successfully uploaded and processed. |
| **Main Flow** | 1. System displays the traced image with bounding boxes around detected characters. 2. System shows each character chip alongside its predicted Modern Tamil equivalent. 3. System displays the confidence percentage for each prediction. 4. System shows the combined Modern Tamil text output. 5. Results are automatically saved to the history database. |
| **Postconditions** | The user has reviewed the recognition results. The results are stored in the database. |

### Use Case 3: View Recognition History

| Field | Description |
|-------|------------|
| **Use Case ID** | UC-03 |
| **Use Case Name** | View Recognition History |
| **Actor** | User / Researcher |
| **Description** | The user browses past recognition sessions stored in the database. |
| **Preconditions** | At least one recognition has been performed previously. |
| **Main Flow** | 1. User navigates to the History page. 2. System retrieves recognition records from the MySQL database. 3. System displays records in reverse chronological order (newest first). 4. Each record shows the original filename, recognized text, number of characters found, and timestamp. 5. User can click on a record to view detailed results. |
| **Postconditions** | The user has reviewed their recognition history. |

### Use Case 4: View Character Map

| Field | Description |
|-------|------------|
| **Use Case ID** | UC-04 |
| **Use Case Name** | View Character Map |
| **Actor** | User / Researcher |
| **Description** | The user browses the complete mapping of all 247 Vatteluttu characters to their Modern Tamil equivalents. |
| **Preconditions** | The system is running and the character mapping data is loaded. |
| **Main Flow** | 1. User navigates to the Character Map page. 2. System displays all 247 characters organized by category. 3. Each entry shows the label code (e.g., va_037), the Modern Tamil character, and the category. 4. User can filter by category (vowels, consonants, compounds, etc.). 5. User can search for specific characters. |
| **Postconditions** | The user has viewed the character mapping information. |

### Use Case 5: Delete History Record

| Field | Description |
|-------|------------|
| **Use Case ID** | UC-05 |
| **Use Case Name** | Delete History Record |
| **Actor** | User / Researcher |
| **Description** | The user deletes a specific recognition history record from the database. |
| **Preconditions** | At least one recognition history record exists. |
| **Main Flow** | 1. User navigates to the History page. 2. User clicks the delete button on a specific record. 3. System asks for confirmation. 4. Upon confirmation, the system deletes the record from the MySQL database. 5. The history list is refreshed. |
| **Postconditions** | The selected record is permanently removed from the database. |

---
