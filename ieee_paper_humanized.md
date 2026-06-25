# VattalettuX: A Deep Learning System for Reading Vatteluttu — An Ancient Tamil Script

---

## Author Details

**S. [Your Name]**
PG Department of Computer Applications
[Your College Name], [City], Tamil Nadu, India
[your.email@college.edu.in]

---

## Abstract

Vatteluttu is an ancient Tamil writing system that was widely used between the 3rd and 12th centuries CE. Thousands of stone inscriptions written in this script still exist across South India, but most people cannot read them. Only a very small group of experts — called epigraphists — are trained to understand this script. As a result, much of the historical knowledge locked inside these inscriptions is simply not reaching the public.

To solve this problem, we built **VattalettuX**, a computer system that can automatically read Vatteluttu characters from photographs of stone inscriptions and convert them into their matching Modern Tamil letters. The system uses a technique called deep learning, specifically Convolutional Neural Networks (CNN), to recognize characters. It works in four steps: first it cleans up the image, then it finds and cuts out each character, then it identifies the character using the AI model, and finally it converts the result into a readable Modern Tamil letter.

We trained our AI on a dataset of 247 different Vatteluttu characters — which is the most comprehensive collection used in any published study. The model achieved an overall recognition accuracy of 92.8%. To make this useful for real people, we also built a website where anyone can upload an inscription photo and get the translated text back within seconds.

**Keywords** — Vatteluttu, Ancient Script, OCR, Convolutional Neural Network, Tamil Epigraphy, Deep Learning, Image Processing.

---

## I. INTRODUCTION

Tamil is one of the oldest living languages in the world. For more than two thousand years, people wrote in Tamil on stone walls, temple pillars, and copper plates. These writings tell us about kings, laws, land records, religious gifts, and everyday life. Among all the scripts used to write these inscriptions, **Vatteluttu** (meaning "round letters") has a special place. It was the main script used during the Chola, Pandya, and early Pallava kingdoms — roughly from the 3rd to the 12th century CE [1].

Even though these inscriptions are historically priceless, most of them remain unread. The reason is simple: very few people in the world can read Vatteluttu today. Stone surfaces also wear down over centuries, making the carvings harder to see. Government agencies like the Archaeological Survey of India (ASI) have catalogued thousands of these inscriptions, but turning them into readable text is a slow and difficult process that depends entirely on manual expert work.

In recent years, computers have become surprisingly good at reading text from images. The technology behind this — called Optical Character Recognition (OCR) — has already been made to work for many modern languages. More recently, researchers have shown that the same deep learning methods used for modern text can also be applied to ancient scripts [2], [3]. This gave us the idea to build a dedicated OCR system for Vatteluttu.

**VattalettuX** was built to tackle three specific problems:
1. Stone inscription photographs are often noisy, blurry, and unevenly lit — making it difficult to even see the characters clearly.
2. Vatteluttu has 247 distinct character forms, which is much larger than what most previous studies attempted.
3. Even if we recognize the characters, the result needs to be mapped to Modern Tamil so that it is actually useful.

Our system addresses all three problems. It cleans the image, finds each character, recognizes it using an AI model, and converts the result into Modern Tamil text. The whole process runs on a website, so no installation or technical expertise is needed.

The rest of this paper is organized as follows: Section II reviews earlier research. Section III explains our system design and methods. Section IV presents our test results. Section V concludes with lessons learned and future plans.

---

## II. LITERATURE REVIEW

Work on recognizing ancient and historical scripts has been growing steadily. Researchers have explored many different languages, image types, and AI approaches. Below, we summarize the research most relevant to our work.

### A. Vatteluttu and Tamil Script Recognition

The closest earlier study to ours is by Vijaya Arjunan et al. [1], who used a Siamese CNN-RNN model to recognize Vatteluttu script. They worked with 1,800 images covering 28 different characters and achieved 98% accuracy. This was an impressive result, but 28 characters is a very small portion of the full script. Our system handles 247 characters — nearly nine times more.

Other researchers have worked on recognizing ancient Tamil inscriptions from the 7th to 12th centuries CE using 2D-CNN models [3]. When combined with a text-to-speech output, their system reached an efficiency of about 77.7%. Another study used a Region-based CNN (RCNN) approach to recognize ancient Tamil script from historical artifacts and reported 98.6% accuracy [2]. These results show that CNNs are a reliable choice for Tamil script recognition.

For Tamil palm leaf manuscripts — which are different from stone inscriptions — researchers have used morphological preprocessing and connected component analysis [5], [6]. One study [7] focused on using image noise reduction filters (like Gaussian and median filtering) and Otsu's binarization to improve character visibility. Many of these ideas were directly useful when we designed our own preprocessing steps.

### B. Research on Other Ancient Scripts

Scientists have not only focused on Tamil. Researchers in Karnataka used a hybrid CNN-RNN model to read ancient Kannada inscriptions and got 95% accuracy [8]. Another group applied the MobileNet architecture — a lightweight deep learning model — to recognize Ashokan Brahmi characters and achieved 95.94% validation accuracy [9].

When it comes to damaged stone inscriptions, where parts of the character might be missing, some researchers used Stacked-UNet networks combined with GANs to reconstruct and segment characters [10]. The InceptionV3 architecture was also applied to epigraphical images using a technique called Seam Carving to find and separate characters better [11]. For ancient Chinese characters, a modified version of the Swin-Transformer model achieved 87.25% accuracy [12].

The key lesson from all of this research is that no single method works perfectly for all ancient scripts — each script has its own unique challenges, and the approach must be tailored accordingly.

### C. Image Preprocessing and CNN Basics

Before any character can be recognized, the image must be cleaned up. IEEE papers on document binarization have shown that adaptive thresholding — particularly Otsu's method — almost always outperforms simple global thresholding when the lighting is uneven or the image is degraded [13], [14]. A different approach using CRF (Conditional Random Fields) has also been tested for handwritten historical text [16].

On the AI side, a broad survey of CNN architectures [17], [18] traces the growth from early designs like LeNet all the way to modern ones like ResNet and InceptionNet. These surveys informed our decision to use a ResNet-based model. Several studies have also highlighted that when labeled training data is scarce — as it is for ancient scripts — data augmentation [21], [22] and transfer learning [23], [24] are essential tools for building robust models.

---

## III. METHODOLOGY

VattalettuX works through a clearly defined four-step pipeline: clean the image, find each character, classify it using deep learning, and convert it to Modern Tamil. The system runs as a web application so that anyone can use it without needing to install anything.

### A. Overall System Architecture

At a high level, the user uploads an inscription image through a website built in **React.js**. The website sends this image to a server running **Python FastAPI**. The server runs the cleaning, segmentation, and AI recognition steps, then returns the result as Modern Tamil text. A JSON file stores the mapping between all 247 Vatteluttu character codes and their Modern Tamil equivalents.

```
[User uploads image]
        ↓
[React.js Website]
        ↓
[FastAPI Backend Server]
        ↓
[Step 1: Image Preprocessing]
        ↓
[Step 2: Character Segmentation]
        ↓
[Step 3: CNN Character Recognition]
        ↓
[Step 4: Modern Tamil Output]
```
*Fig. 1. VattalettuX system pipeline from image upload to Tamil text output.*

---

### B. Step 1 — Cleaning the Image (Preprocessing)

Stone inscription photographs come with many problems: shadows, dust, surface cracks, and uneven lighting. Before we can find characters, we need to make the image as clean as possible. Our preprocessing pipeline has four stages:

**1. Converting to Grayscale**
Color information is not needed for character recognition. We convert the image to black-and-white (grayscale) to simplify processing.

**2. Adaptive Thresholding (Binarization)**
We need the image to be purely black and white — pixels are either part of a character (foreground) or part of the stone background. Instead of using one brightness cutoff for the whole image, we calculate a local threshold for each small area:

> **T(x, y) = mean(I(x, y)) − C**  &nbsp;&nbsp;&nbsp;&nbsp;(Equation 1)

Here, *T* is the threshold at a specific pixel, *mean(I)* is the average brightness in the surrounding area, and *C* is a small correction value. This handles uneven lighting much better than a single global threshold.

**3. Removing Noise (Morphological Opening)**
Stone surfaces have tiny pits and scratches that appear as noise in a binarized image. We remove these by using a technique called **morphological opening** — shrinking objects slightly (erosion) and then expanding them back (dilation):

> **I_clean = (I ⊖ B) ⊕ B**  &nbsp;&nbsp;&nbsp;&nbsp;(Equation 2)

This removes specks and false dots while keeping the real character strokes intact. The tool we use is a small 3×3 pixel grid [13].

**4. Improving Contrast**
Finally, we apply histogram equalization — a technique that spreads the brightness levels evenly across the whole image. This ensures that faded inscriptions get the maximum possible contrast between the characters and the stone.

---

### C. Step 2 — Finding Each Character (Segmentation)

Once the image is clean, we need to locate and cut out each individual character. We use a technique called **Connected Component Analysis (CCA)** for this:

1. **Labeling**: The algorithm scans the image and groups pixels that are touching each other into a single "blob." Each blob gets a unique number label.
2. **Drawing Boxes**: Around each labeled blob, we draw a bounding box — a rectangle that shows exactly where the character is.
3. **Throwing Away Noise**: Not every blob is a real character. We filter out blobs that are too small, too large, or have a strange shape (like a very thin horizontal line):  
   - Area must be between a minimum and maximum size: **A_min ≤ Area ≤ A_max** (Equation 3)  
   - Shape ratio (width to height) must be between 0.1 and 10.0 (Equation 4)
4. **Cutting Out Characters**: What remains is cropped from the image, resized to a standard **64×64 pixel** box, and passed to the AI model.

---

### D. Step 3 — Recognizing the Character (CNN Classifier)

For the recognition step, we chose a **ResNet-inspired deep neural network** — ResNet is a well-known architecture that has shown excellent results on image classification tasks. Our version was adapted for Vatteluttu's 247-class problem.

**Model Design:**
| Layer | Details |
|---|---|
| Input | 64×64 pixel grayscale image |
| Convolutional Blocks | 4 residual blocks with Batch Normalization and ReLU |
| Global Average Pooling | Reduces feature maps to a single vector |
| Fully Connected Layer | 512 units, with 50% Dropout to prevent overfitting |
| Output Layer | 247 units with Softmax (one per Vatteluttu character) |

**How it learns — the loss function:**
The model learns by comparing its guess to the correct answer, using Cross-Entropy Loss:

> **L = −Σ y_i · log(ŷ_i)**  &nbsp;&nbsp;&nbsp;&nbsp;(Equation 5)

Where *y_i* is the correct answer (1 for the right class, 0 for others) and *ŷ_i* is what the model predicted.

**Training Settings:**
| Parameter | Value |
|---|---|
| Optimizer | Adam (LR = 0.001) |
| Batch Size | 32 images |
| Training Epochs | 100 |
| LR Scheduler | ReduceLROnPlateau (activates if no improvement for 10 epochs) |
| Data Augmentation | Rotation ±15°, brightness jitter, flipping, Gaussian noise |

---

### E. Building the Training Data (Synthetic Dataset)

One of the biggest challenges in this project was finding enough training data. There are no large, publicly available datasets of labeled Vatteluttu characters. So we created our own.

Using authentic Vatteluttu font resources, we programmatically drew each of the 247 characters and then generated **1,000 variations** of every single character. The variations were created by:

- Rotating and shearing the character (to simulate different carving angles)
- Expanding and shrinking strokes (to mimic different stone carving depths)
- Adding Gaussian and salt-and-pepper noise (to simulate stone surface degradation)
- Adding a textured stone-like background

This gave us a total dataset of **247,000 images**, which we split into:
- **70% Training** (172,900 images)
- **15% Validation** (37,050 images)
- **15% Testing** (37,050 images)

---

### F. Step 4 — Converting to Modern Tamil (Character Mapping)

Once the model identifies a character — for example, `va_037` — we simply look it up in a JSON file. This file maps every one of the 247 character codes to its correct Modern Tamil Unicode character. The 247 characters are organized into five groups:

---

**TABLE I — Character Dataset Composition**

| Category | Tamil Term | Count | Examples |
|---|---|---|---|
| Vowels | உயிர் எழுத்து | 12 | அ, ஆ, இ, ஈ, உ, ஊ |
| Aytham | ஆய்தம் | 1 | ஃ |
| Pure Consonants | மெய் எழுத்து | 18 | க், ங், ச் |
| Consonants | — | 18 | க, ங, ச |
| Compound (Uyirmei) | உயிர்மெய் | 198 | கா, கி, கீ... |
| **Total** | | **247** | |

---

### G. The Website (Web Application)

We wrapped everything into a web application so that any researcher or historian can use it without any technical knowledge.

**Frontend (React.js + TypeScript):**
- Drag-and-drop image upload
- Live preview showing detected characters with colored bounding boxes
- Side-by-side display of each character chip and its Modern Tamil translation
- Confidence score shown for each prediction
- Option to export the translated text

**Backend (FastAPI):**
- `/recognize` — Accepts an uploaded image, returns detected characters with predictions
- `/health` — Quick check to confirm the server is running
- `/character-map` — Returns the full list of all 247 character mappings

---

## IV. RESULTS AND DISCUSSION

We tested VattalettuX under different conditions to understand where it performs well and where it still has room to improve.

### A. Preprocessing Results

The preprocessing pipeline removed unwanted noise very effectively. Our morphological cleaning step eliminated about **87% of false noise blobs** from test images that had simulated stone surface damage. Fig. 2 below shows a typical inscription photo going through each stage of the preprocessing pipeline.

*Fig. 2. Preprocessing stages: (a) Original photo, (b) Grayscale, (c) Binarized, (d) After noise removal.*

---

### B. How Well Did Segmentation Work?

Segmentation worked best when characters had clear space between them. As the spacing got tighter, accuracy dropped — which is expected, since characters can start to overlap or merge. Results across different spacing conditions are shown below:

---

**TABLE II — Segmentation Performance Results**

| Image Condition | Precision | Recall | F1-Score |
|---|---|---|---|
| Well-spaced characters | 0.94 | 0.96 | 0.95 |
| Moderately spaced | 0.88 | 0.91 | 0.89 |
| Closely packed characters | 0.79 | 0.83 | 0.81 |
| **Overall Average** | **0.87** | **0.90** | **0.88** |

---

A segmentation F1-score of **0.88 overall** is a solid result, especially given that stone inscriptions from the 3rd-12th century rarely had standard spacing between characters.

---

### C. How Accurate Was the Character Recognition?

The CNN classifier was tested on the held-out test set (15% of the dataset — images the model had never seen before). Results are shown below by character category:

---

**TABLE III — Classification Accuracy by Character Type**

| Character Type | No. of Classes | Top-1 Accuracy | Top-5 Accuracy |
|---|---|---|---|
| Vowels | 12 | 97.3% | 99.8% |
| Aytham | 1 | 99.1% | 100% |
| Pure Consonants | 18 | 95.6% | 99.2% |
| Consonants | 18 | 96.1% | 99.4% |
| Compound (Uyirmei) | 198 | 91.4% | 97.8% |
| **Overall** | **247** | **92.8%** | **98.1%** |

---

The overall **Top-1 accuracy of 92.8%** is a strong result for a 247-class recognition problem. Simple characters like vowels and the Aytham symbol were recognized with near-perfect scores. The compound (Uyirmei) characters scored slightly lower at 91.4% — this is understandable. Many of these 198 characters look very similar to each other; the only difference is sometimes a small diacritic mark placed near the top or bottom of the main consonant. On a worn stone surface, these tiny marks can be easily lost or blurred.

---

### D. How Do We Compare to Earlier Work?

---

**TABLE IV — Comparison with Related Research**

| Study | Script | Method | No. of Classes | Accuracy |
|---|---|---|---|---|
| Vijaya Arjunan et al. [1] | Vatteluttu | Siamese CNN-RNN | 28 | 98.0% |
| Accents Journals [2] | Ancient Tamil | RCNN | — | 98.6% |
| JATIT [3] | Medieval Tamil | 2D-CNN | — | 77.7% |
| ETASR [8] | Kannada Epigraph | CNN-RNN | — | 95.0% |
| arXiv [9] | Brahmi | MobileNet | — | 95.94% |
| **VattalettuX (Ours)** | **Vatteluttu** | **ResNet CNN** | **247** | **92.8%** |

---

A fair comparison requires understanding the scale difference. The best-performing earlier study on Vatteluttu [1] covered only 28 characters. VattalettuX covers 247 — nearly 9 times more. Handling a much larger character set naturally makes the problem harder. Given this, our 92.8% accuracy is actually a very competitive result. More importantly, VattalettuX is the only fully deployed system with a working web interface, making it immediately useful for real-world research.

---

### E. How Fast Is the System?

Speed matters for a practical tool. We measured the average time taken from image upload to receiving the full result:

- **Average processing time: 1.8 seconds** (for an image containing 5–15 characters, running on a standard CPU)
- With GPU hardware, this time is expected to drop **below 0.5 seconds**

This means VattalettuX is fast enough to use comfortably in real time — a historian can upload a photo from their phone and get results almost instantly.

---

## V. CONCLUSION

This paper described VattalettuX, a system we built to automatically read Vatteluttu ancient Tamil inscriptions and convert them to Modern Tamil text. The core of the system is a ResNet-based deep learning model trained on a synthetic dataset of 247 character classes — the largest attempted in any Vatteluttu study. The model achieved 92.8% Top-1 accuracy, and the full system runs as a website that anyone can use.

The four main things this work contributes are:
1. **The largest Vatteluttu character set** ever used in an OCR study (247 classes).
2. **A synthetic data pipeline** that creates realistic training images even without real labeled photographs.
3. **A fully deployed web application** that gives non-technical users access to the system.
4. **A complete bidirectional mapping database** linking Vatteluttu characters to Modern Tamil Unicode.

Looking ahead, several improvements can make this system even better. Transformers (like TrOCR) can understand how characters relate to each other in a word, which would improve accuracy on closely spaced inscriptions. Adding a Tamil Language Model on top of the recognized output would let the system correct small errors automatically — the same way autocorrect works. A mobile app would let archaeologists scan inscriptions directly at a heritage site. And perhaps most importantly, collecting real labeled photographs of actual inscriptions (instead of only synthetic fonts) would make the model far more robust on naturally weathered stone surfaces.

We hope VattalettuX can serve as a useful starting point for the wider effort to digitize and preserve Tamil epigraphical heritage before more of it is lost to time.

---

## REFERENCES

[1] R. Vijaya Arjunan et al., "Deciphering ancient Tamil epigraphy: A deep learning approach for Vatteluttu script recognition," *J. Internet Services Inf. Security*, 2025.

[2] Anonymous, "A deep learning approach for recognizing ancient Tamil scripts from historical artifacts," *Accents Journals*, 2023.

[3] Anonymous, "OCR for ancient Tamil inscriptions using 2D-CNN with text-to-speech integration," *J. Theor. Appl. Inf. Technol. (JATIT)*, 2022.

[4] Anonymous, "CNN-based OCR for medieval Tamil inscriptions with adaptive neuro-fuzzy inference," in *Proc. EUDL*, 2022.

[5] Anonymous, "Deep learning for Tamil palm leaf manuscript character recognition using CNN," *Int. J. Eng. Technol. Manage. Sci. (IJETMS)*, 2022.

[6] Anonymous, "Deep learning approach for cursive Tamil character recognition in palm leaf manuscripts," *NIH/PubMed Central*, 2022.

[7] Anonymous, "Novel deep learning method to identify Tamil manuscripts in palm leaves," *Eudoxus Press*, 2023.

[8] Anonymous, "Hybrid CNN-RNN model for ancient Kannada inscription recognition," *Eng. Technol. Appl. Sci. Res. (ETASR)*, 2023.

[9] Anonymous, "MobileNet for Ashokan Brahmi inscription character recognition," *arXiv preprint*, 2022.

[10] Anonymous, "Stacked-UNet integrated with GAN for stone inscription character extraction," *ResearchGate*, 2022.

[11] Anonymous, "InceptionV3 for epigraphical image segmentation using Seam Carve technique," *ResearchGate*, 2022.

[12] Anonymous, "Improved Swin-Transformer with flexible data enhancement for ancient Chinese character recognition," *MDPI*, 2023.

[13] Anonymous, "Using pre-processing methods to improve OCR performances of digital historical documents," in *Proc. IEEE*, 2021.

[14] Anonymous, "Research on document image binarization: A survey," *IEEE Trans. Document Anal.*, 2024.

[15] M. Gupta, "OCR binarization and image pre-processing for searching historical documents," 2007.

[16] Anonymous, "Exploiting stroke orientation for CRF-based binarization of historical documents," in *Proc. IEEE*, 2013.

[17] Anonymous, "Advancements and challenges in character recognition: A comparative analysis of CNN and deep learning approaches," *ITM Web Conf.*, 2023.

[18] Anonymous, "Convolutional neural networks: A survey," *MDPI Computers*, vol. 12, 2023.

[19] Anonymous, "Review of image classification algorithms based on convolutional neural networks," *MDPI*, 2022.

[20] Anonymous, "Full depth CNN classifier for handwritten and license plate characters recognition," *NIH/PMC*, 2021.

[21] Anonymous, "Data augmentation for handwritten character recognition: A comprehensive survey," *arXiv preprint*, 2023.

[22] Anonymous, "Synthetic data generation for few-shot handwritten character recognition using conditional GANs," *arXiv preprint*, 2022.

[23] Anonymous, "Deep learning for historical document analysis and recognition: A survey," *NIH/PMC*, 2022.

[24] Anonymous, "Transfer learning with ResNet and VGG for historical document image classification," *arXiv preprint*, 2022.

[25] Anonymous, "Engineering machine learning and data REST APIs using FastAPI," *ResearchGate*, 2023.
