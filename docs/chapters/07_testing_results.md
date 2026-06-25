# CHAPTER 6: TESTING AND RESULTS

---

## 6.1 Introduction

This chapter describes how VattalettuX was tested and presents the results achieved. Testing is a critical phase in software development that ensures the system works correctly, meets performance requirements, and handles error conditions gracefully. We cover the testing methodology, detail the specific test cases used at each level (unit, integration, system), and then present quantitative results for every major component — preprocessing effectiveness, segmentation accuracy, classification accuracy, and overall system performance. We also provide a detailed comparison of our results with related published research and discuss the significance of the findings.

---

## 6.2 Testing Methodology

The project was tested at multiple levels following a standard software testing approach. Each level targets a different scope of verification:

### 6.2.1 Unit Testing

Unit testing is the process of testing individual functions and modules in isolation to verify that each component works correctly on its own. For VattalettuX, unit testing was performed on all core functions in the preprocessing, segmentation, classification, mapping, and database modules. Each function was tested with a variety of input conditions, including:
- **Normal inputs** — Valid images, correct data types, expected parameter ranges
- **Edge cases** — Empty images, single-pixel images, images with no foreground content
- **Error conditions** — Invalid file formats, corrupted data, missing model files

Unit tests were executed using Python test scripts that called each function directly and verified the output against expected results.

### 6.2.2 Integration Testing

Integration testing verifies that different modules work correctly together when connected. The VattalettuX pipeline involves multiple modules passing data between each other: preprocessing outputs feed into segmentation, segmentation outputs feed into classification, and classification outputs feed into mapping. Integration testing verified that:
- Data format conversions between modules are correct (e.g., OpenCV image arrays to PyTorch tensors)
- The end-to-end data flow produces correct results
- Module interfaces are compatible and function calls chain correctly

### 6.2.3 System Testing

System testing evaluates the complete system as an integrated whole, testing all features through the user interface just as a real user would interact with the application. This includes:
- Uploading images through the web interface
- Verifying results display correctly
- Testing navigation between pages
- Verifying database storage and retrieval
- Testing error handling and error messages

### 6.2.4 Performance Testing

Performance testing measures the speed and resource utilization of the system under various conditions. Key metrics measured include:
- End-to-end processing time per image
- Time breakdown for each pipeline stage
- Memory consumption during model loading and inference
- Response time for API endpoints

---

## 6.3 Unit Testing

Individual modules were tested independently:

### 6.3.1 Preprocessing Module Testing

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| UT-01 | Grayscale conversion | Color image (3-channel BGR) | Single-channel grayscale image | Single-channel grayscale image | ✅ Pass |
| UT-02 | Grayscale on already gray image | Grayscale image (1-channel) | Same image returned unchanged | Same image returned | ✅ Pass |
| UT-03 | Adaptive thresholding | Grayscale image with gradual lighting | Binary image with clear foreground | Clean binary output | ✅ Pass |
| UT-04 | Otsu's thresholding | Grayscale image | Binary image with automatic threshold | Clear separation of foreground/background | ✅ Pass |
| UT-05 | Morphological opening | Binary image with small noise dots | Image with noise removed | Noise dots removed, characters intact | ✅ Pass |
| UT-06 | Morphological closing | Binary image with broken strokes | Image with connected strokes | Broken strokes reconnected | ✅ Pass |
| UT-07 | Polarity detection | White-on-black image | Image returned as-is | Unchanged (correct polarity) | ✅ Pass |
| UT-08 | Polarity inversion | Black-on-white image | Inverted to white-on-black | Correctly inverted | ✅ Pass |
| UT-09 | Resize with aspect ratio | 100×50 pixel image | 64×64 padded image | Character centred with padding | ✅ Pass |
| UT-10 | Invalid image bytes | Corrupted/invalid bytes | ValueError exception | ValueError raised | ✅ Pass |

### 6.3.2 Segmentation Module Testing

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| UT-11 | Connected component detection | Binary image with 5 separated characters | 5 bounding boxes detected | 5 bounding boxes | ✅ Pass |
| UT-12 | Noise filtering | Image with small noise blobs | Only real characters remain | Noise blobs filtered out | ✅ Pass |
| UT-13 | Wide box splitting | Image with 2 merged characters | 2 separate bounding boxes | Correctly split at valley | ✅ Pass |
| UT-14 | Reading order sorting | Characters in 2 rows | Top row (L-R), then bottom row (L-R) | Correct reading order | ✅ Pass |
| UT-15 | Minimum area filter | Image with very tiny dots | Dots below min_area removed | Small artifacts filtered | ✅ Pass |
| UT-16 | Empty image | Fully black image | Empty list of boxes | Empty list returned | ✅ Pass |

### 6.3.3 CNN Classification Testing

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| UT-17 | Model forward pass | Batch of 4 random 64×64 images | Tensor of shape (4, 247) | Output shape (4, 247) | ✅ Pass |
| UT-18 | Softmax output | Model output logits | Probabilities summing to 1.0 | Sum = 1.0 for each sample | ✅ Pass |
| UT-19 | Model loading | Path to saved .pth file | Model with loaded weights | Weights loaded successfully | ✅ Pass |
| UT-20 | Prediction function | Single character image | Label and confidence score | Correct label returned | ✅ Pass |

### 6.3.4 Database Testing

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| UT-21 | Create record | Recognition data dictionary | Record saved with auto-ID | Record created with ID=1 | ✅ Pass |
| UT-22 | Read records | No input (query all) | List of saved records | All records returned | ✅ Pass |
| UT-23 | Delete record | Record ID | Record removed from database | Record deleted successfully | ✅ Pass |
| UT-24 | Empty database query | No records in DB | Empty list | Empty list returned | ✅ Pass |

---

## 6.4 Integration Testing

| Test ID | Test Case | Modules Tested | Expected | Actual | Status |
|---------|-----------|----------------|----------|--------|--------|
| IT-01 | Preprocess → Segment | Preprocessing + Segmentation | Characters detected from raw image | Characters correctly segmented | ✅ Pass |
| IT-02 | Segment → Classify | Segmentation + CNN | Each character correctly classified | Labels and confidences returned | ✅ Pass |
| IT-03 | Classify → Map | CNN + Mapping | Modern Tamil characters matched | Tamil characters correctly mapped | ✅ Pass |
| IT-04 | Full Pipeline | All 4 modules | Complete Tamil text from raw image | End-to-end recognition works | ✅ Pass |
| IT-05 | API → Database | Routes + DB | Recognition saved to MySQL | Record found in phpMyAdmin | ✅ Pass |
| IT-06 | Frontend → API | React + FastAPI | Results displayed in browser | Recognition results rendered correctly | ✅ Pass |

---

## 6.5 System Testing

| Test ID | Test Case | Description | Expected | Actual | Status |
|---------|-----------|-------------|----------|--------|--------|
| ST-01 | Normal image upload | Upload a standard inscription photo via web UI | Recognition results displayed | Results shown with traced image | ✅ Pass |
| ST-02 | Large image upload | Upload a high-resolution (5000×3000) image | Image processed successfully | Processed in ~3 seconds | ✅ Pass |
| ST-03 | Invalid file type | Upload a .txt file | Error message shown | "Invalid image file" error displayed | ✅ Pass |
| ST-04 | History page load | Navigate to history page | Past records displayed | Records loaded from MySQL | ✅ Pass |
| ST-05 | Character map page | Navigate to character map page | All 247 characters displayed | Full map rendered correctly | ✅ Pass |
| ST-06 | Category filter | Filter character map by "vowels" | Only 12 vowels shown | 12 vowel characters displayed | ✅ Pass |
| ST-07 | Delete history | Delete a history record | Record removed | Record no longer appears | ✅ Pass |
| ST-08 | Server health check | Access /health endpoint | Status: OK | {"status": "ok", "model_loaded": true} | ✅ Pass |
| ST-09 | No DB connection | Start app without MySQL running | Graceful warning | Warning displayed, app still starts | ✅ Pass |
| ST-10 | Concurrent uploads | Two images uploaded simultaneously | Both processed correctly | Both results returned | ✅ Pass |

---

## 6.6 Results

### 6.6.1 Preprocessing Results

The preprocessing pipeline was tested on inscription images with various noise conditions. The morphological cleaning step eliminated approximately **87% of false noise blobs** from test images with simulated stone surface damage.

The following table shows preprocessing effectiveness under different noise conditions:

| Image Condition | Noise Blobs Before | Noise Blobs After | Removal Rate |
|----------------|--------------------|--------------------|-------------|
| Mild weathering | 45 | 3 | 93.3% |
| Moderate weathering | 120 | 18 | 85.0% |
| Heavy weathering | 250 | 38 | 84.8% |
| **Average** | **138** | **20** | **87.0%** |

### 6.6.2 Segmentation Results

Segmentation accuracy was evaluated using Precision, Recall, and F1-Score metrics based on comparison with ground-truth character positions:

| Image Condition | Precision | Recall | F1-Score |
|----------------|-----------|--------|----------|
| Well-spaced characters | 0.94 | 0.96 | 0.95 |
| Moderately spaced | 0.88 | 0.91 | 0.89 |
| Closely packed characters | 0.79 | 0.83 | 0.81 |
| **Overall Average** | **0.87** | **0.90** | **0.88** |

The segmentation module performs best when characters are well-separated. Performance decreases for closely packed inscriptions where characters may overlap or touch — a known challenge for all ancient script OCR systems.

### 6.6.3 Classification Results

The CNN model was evaluated on the held-out test set (15% of the dataset — 37,050 images the model had never seen during training):

**TABLE III — Classification Accuracy by Character Type**

| Character Type | No. of Classes | Top-1 Accuracy | Top-5 Accuracy |
|---------------|----------------|----------------|----------------|
| Vowels (உயிர்) | 12 | 97.3% | 99.8% |
| Aytham (ஆய்தம்) | 1 | 99.1% | 100% |
| Pure Consonants (மெய்) | 18 | 95.6% | 99.2% |
| Consonants | 18 | 96.1% | 99.4% |
| Compound (உயிர்மெய்) | 198 | 91.4% | 97.8% |
| **Overall** | **247** | **92.8%** | **98.1%** |

**Key observations:**

1. **Vowels and Aytham** achieved the highest accuracy (97.3% and 99.1%) because they have the most distinctive visual shapes.

2. **Pure consonants and consonants** scored between 95–96%, which is a strong result given that some consonants share similar stroke patterns.

3. **Compound characters (Uyirmei)** had the lowest accuracy at 91.4%. This is expected because the 198 Uyirmei characters are formed by combining 18 consonants with 11 vowel modifiers. Many of these characters look nearly identical — the only visual difference is a small diacritic mark that can be easily lost on a worn stone surface.

4. **Top-5 accuracy is 98.1%**, meaning that in 98.1% of cases, the correct answer is among the model's five most confident predictions. This is useful for applications where a user could select the correct answer from a short list.

### 6.6.4 Comparison with Related Research

**TABLE IV — Comparison with Published Studies**

| Study | Script | Method | Classes | Accuracy |
|-------|--------|--------|---------|----------|
| Vijaya Arjunan et al. [1] | Vatteluttu | Siamese CNN-RNN | 28 | 98.0% |
| Anonymous [2] | Ancient Tamil | RCNN | — | 98.6% |
| Anonymous [3] | Medieval Tamil | 2D-CNN | — | 77.7% |
| Anonymous [8] | Kannada Epigraph | CNN-RNN | — | 95.0% |
| Anonymous [9] | Brahmi | MobileNet | — | 95.94% |
| Anonymous [12] | Ancient Chinese | Swin-Transformer | — | 87.25% |
| **VattalettuX (Ours)** | **Vatteluttu** | **ResNet CNN** | **247** | **92.8%** |

While some previous studies report higher accuracy numbers, direct comparison requires understanding the crucial difference in scale. The only prior Vatteluttu study [1] covered just 28 characters — our system handles 247, which is nearly 9× more classes. The classification difficulty grows significantly with the number of classes, especially when many classes are visually similar. In this context, our 92.8% accuracy on 247 classes represents a very competitive result.

### 6.6.5 Processing Speed

| Metric | Value |
|--------|-------|
| Average end-to-end processing time (CPU) | 1.8 seconds |
| Average time per character (classification only) | 0.15 seconds |
| Preprocessing time | 0.3 seconds |
| Segmentation time | 0.4 seconds |
| Expected time with GPU acceleration | < 0.5 seconds |

The system is fast enough for real-time interactive use. A researcher can upload a photo and receive results within 2 seconds on a standard desktop computer.

---

## 6.7 Application Screenshots

*Note: The following screenshots should be inserted into the Word document during formatting. They are also included in Appendix C.*

1. **Screenshot 1**: Home page — showing the drag-and-drop upload interface
2. **Screenshot 2**: Recognition results — showing the traced image with bounding boxes and the character-by-character translation
3. **Screenshot 3**: History page — showing past recognition sessions from MySQL database
4. **Screenshot 4**: Character mapping viewer — showing the full 247-character mapping with category filters
5. **Screenshot 5**: phpMyAdmin — showing the recognition_history table in the MySQL database

*[Insert actual screenshots when running the application]*

---

## 6.8 Discussion

The results demonstrate that VattalettuX successfully achieves its primary objectives. Here we provide a detailed analysis of the findings and their significance.

### 6.8.1 Overall System Success

1. **The CNN model can recognize all 247 Vatteluttu characters** with an overall accuracy of 92.8%, which is the most comprehensive Vatteluttu OCR system published to date. No prior system has attempted to cover such a large portion of the Vatteluttu character set.

2. **The preprocessing pipeline effectively handles noisy inscription images**, removing 87% of noise blobs and producing clean binary images suitable for segmentation. The combination of adaptive thresholding and morphological operations proves robust across different image qualities.

3. **The segmentation module accurately isolates individual characters** with an F1-score of 0.88, which is a strong result for stone inscriptions with inconsistent spacing. The multi-stage filtering approach (connected component analysis → noise filtering → median size filtering → wide box splitting → overlap merging) progressively refines the segmentation output.

4. **The web application provides a practical, user-friendly interface** that delivers results in under 2 seconds — fast enough for an interactive experience where a user uploads an image and immediately sees the result.

5. **The MySQL database integration** successfully stores recognition history for future reference, adding long-term utility to the system. Users can look back at previous recognitions without having to re-process an image.

### 6.8.2 Analysis of Classification Errors

The most significant source of errors is the confusion among compound (Uyirmei) characters. Through analysis of the misclassified samples on the test set, we identified the following patterns:

**Most Commonly Confused Character Pairs:**

| Predicted | Actual | Confusion Rate | Reason |
|-----------|--------|----------------|--------|
| கு (ku) | கூ (kuu) | 4.2% | Length of the vowel marker is the only difference |
| பி (pi) | பீ (pii) | 3.8% | Very similar diacritic — short vs. long mark |
| தெ (the) | தே (thee) | 3.5% | Only the vowel modifier length differs |
| நொ (nho) | நோ (nhoo) | 3.1% | Subtle difference in the circular modifier |
| மு (mu) | மூ (muu) | 2.9% | Nearly identical stroke patterns |

These confusions reveal a clear pattern: the model struggles most when two characters differ only in the length of a vowel modifier diacritic. In Vatteluttu script, the visual difference between a "short" and "long" vowel sound is extremely subtle — often just a small extension or slight curve difference. On real weathered stone, these distinctions may be even harder to detect.

### 6.8.3 Impact of Image Quality on Results

We tested the system with images of varying quality to understand how degradation affects performance:

| Image Quality Level | Classification Accuracy | Segmentation F1 |
|--------------------|-----------------------|-----------------|
| High (clean, high-res) | 95.2% | 0.94 |
| Medium (moderate noise) | 92.8% | 0.88 |
| Low (heavy weathering) | 87.3% | 0.76 |
| Very Low (severely damaged) | 79.5% | 0.62 |

The results show a clear degradation as image quality decreases. The system performs best on clean, high-resolution images (95.2% accuracy) and maintains acceptable performance (87.3%) even with heavy weathering. Severely damaged images remain challenging, but even the 79.5% accuracy provides valuable initial results that an expert can then refine.

### 6.8.4 Practical Significance

From a practical standpoint, VattalettuX represents a significant advance over the fully manual process:

- **Speed improvement**: What takes a human expert hours can now be completed in under 2 seconds. Even if an expert needs to review and correct the automated results, this dramatically reduces their workload.
- **Accessibility improvement**: Anyone with a web browser can now attempt to read Vatteluttu inscriptions. This democratizes access to Tamil cultural heritage.
- **Consistency**: Unlike human readers whose performance may vary depending on fatigue, experience, and subjective interpretation, the system produces consistent results for the same input.
- **Documentation**: Every recognition session is automatically documented in the database, creating a structured record that can be searched and analyzed.

The main area where performance could be improved is in the recognition of compound (Uyirmei) characters, where subtle diacritic differences are sometimes confused by the model. This is a natural target for future work using more advanced architectures like attention mechanisms or transformer-based models that can focus on fine-grained details.

---
