# CHAPTER 2: LITERATURE SURVEY

---

## 2.1 Introduction

Before building any technical system, it is essential to study what other researchers have already done in the same or related areas. This chapter reviews the existing body of research that is relevant to VattalettuX. The review covers four main areas: (1) recognition of Vatteluttu and other Tamil scripts, (2) recognition of other ancient scripts from around the world, (3) image preprocessing techniques used for degraded historical documents, and (4) convolutional neural network architectures used for image classification. At the end of this chapter, we identify the specific gaps in the existing research that our project aims to fill.

---

## 2.2 OCR Technology — A Brief Overview

Optical Character Recognition (OCR) is the technology that allows computers to read text from images. In its simplest form, OCR takes a photograph or scan of a document, identifies the text characters in it, and converts them into machine-readable digital text. The general OCR pipeline typically consists of four stages:

1. **Preprocessing**: The raw image is cleaned and enhanced — converting to grayscale, removing noise, adjusting contrast, and binarizing (converting to black and white) to clearly separate text from background.

2. **Segmentation**: The preprocessed image is analyzed to locate and isolate each individual character or word. This can involve detecting text regions, splitting lines into words, and words into individual characters.

3. **Feature Extraction and Classification**: Each isolated character image is analyzed to extract visual features (edges, shapes, curves, intersections), and these features are used by a classifier to determine which character it is. In traditional OCR, hand-crafted features like Histogram of Oriented Gradients (HOG) or Scale-Invariant Feature Transform (SIFT) were used. In modern OCR, deep learning models — particularly Convolutional Neural Networks (CNNs) — learn these features automatically from data.

4. **Post-processing**: The recognized characters are assembled into words and sentences. Language models, dictionaries, and grammar rules are applied to correct errors and improve accuracy.

OCR has been around for several decades and has reached near-perfect accuracy for printed text in major modern languages like English, Chinese, Hindi, and Modern Tamil. Commercial products like Google Lens, Adobe Acrobat OCR, and ABBYY FineReader can achieve 99%+ accuracy on standard printed documents.

However, OCR for ancient and historical scripts is a fundamentally different and much harder problem. Unlike modern printed text, which uses standardized fonts and is printed on clean white paper, ancient inscriptions are carved on stone, scratched on palm leaves, or painted on walls. The "writing surface" itself introduces countless challenges:

- **Surface Degradation**: Stone inscriptions are exposed to centuries of weathering. Rain, wind, moss, lichens, and human activity gradually erode the carved surfaces. What was once a deep, clear carving may now be barely visible.
- **Non-uniform Lighting**: Photographs taken at archaeological sites often have harsh shadows, uneven sunlight, and reflections that create dramatic variations in brightness across the image.
- **Physical Damage**: Cracks, chips, and missing fragments are common. Parts of characters may be completely absent due to breakage.
- **No Standard Spacing**: Unlike modern printed text with fixed spacing, ancient inscriptions were carved freehand with variable spacing between characters. Characters may be closely packed, widely spaced, or even overlapping.
- **Large Character Sets**: Many ancient scripts have complex character sets with hundreds of distinct characters, far more than the 26 letters of English or the 46 basic characters of Modern Tamil.
- **Lack of Training Data**: There are no large, publicly available labeled datasets for most ancient scripts. Unlike modern languages where millions of labeled images are available, ancient script researchers typically work with datasets of just a few hundred to a few thousand images.

Despite these challenges, the rapid advancement of deep learning — particularly Convolutional Neural Networks (CNNs) — has opened new possibilities. When researchers can assemble sufficient training data (even through synthetic generation), deep learning models can learn to recognize characters from even highly degraded images. This has led to a growing body of work on applying OCR to ancient scripts from civilizations around the world.

---

## 2.3 Vatteluttu and Tamil Script Recognition

### 2.3.1 Vatteluttu Script Recognition

The research most directly related to our project is the work by **Vijaya Arjunan et al. (2025)** [1], who developed a Siamese CNN-RNN model specifically for Vatteluttu script recognition. The Siamese architecture works by comparing two images side-by-side: the model learns whether a pair of images represents the same character class or different classes. Their system used a CNN for spatial feature extraction from each image and an RNN (Recurrent Neural Network) for modeling sequential dependencies. They worked with a dataset of 1,800 images covering 28 different Vatteluttu characters and achieved an impressive accuracy of 98%.

However, 28 characters represent only about 11% of the full 247-character Vatteluttu alphabet. The relatively high accuracy can be partly attributed to the small number of classes — with only 28 classes, the visual differences between any two characters are likely to be substantial. Our system handles 247 characters — nearly nine times more — which makes the classification problem significantly more challenging because many characters (especially within the 198 compound character group) look nearly identical.

### 2.3.2 Ancient Tamil Inscription Recognition

**Anonymous (2023)** [2] used a **Region-based CNN (RCNN)** approach to recognize ancient Tamil script from historical artifacts such as coins, seals, and pottery. The RCNN architecture first uses a Region Proposal Network (RPN) to identify candidate regions in an image where characters might be located. Each proposed region is then individually classified using a CNN. This two-stage approach (detect then classify) is well-suited for situations where characters are scattered across an image at unpredictable locations. They reported a high accuracy of 98.6%. However, the study focused on well-preserved artifacts (which typically have clearer character impressions than weathered stone) and the number of character classes handled was not specified in detail.

**Anonymous (2022)** [3] worked on OCR for ancient Tamil inscriptions dating from the 7th to 12th centuries CE. They used a **2-dimensional CNN (2D-CNN)** model and integrated a text-to-speech output module so that the recognized text could also be heard by the user. Their combined system achieved an efficiency of approximately 77.7%. While the text-to-speech feature was a creative addition, the relatively low accuracy suggests that the model struggled with the visual complexity of the characters or limitations in the training data.

### 2.3.3 Tamil Palm Leaf Manuscript Recognition

Palm leaf manuscripts are another important category of historical Tamil documents. Unlike stone inscriptions, palm leaves are engraved with a thin stylus and then rubbed with a dark substance to make the text visible. Several researchers have explored applying deep learning to this domain.

**Anonymous (2022)** [5] applied **deep learning with CNN** to recognize Tamil characters from palm leaf manuscripts. They used morphological preprocessing and connected component analysis to prepare the images before classification. A separate study by **Anonymous (2022)** [6] focused specifically on **cursive Tamil characters** in palm leaf manuscripts, which are particularly challenging because strokes often flow into one another. Another study by **Anonymous (2023)** [7] proposed a novel deep learning approach for identifying Tamil manuscripts in palm leaves, using image noise reduction filters such as Gaussian filtering and median filtering, along with Otsu's binarization to improve character visibility before classification.

These palm leaf manuscript studies provided valuable insights into preprocessing techniques that are also applicable to stone inscriptions. While the writing surface is different (leaf versus stone), both domains share the challenge of degraded writing that has survived centuries of natural deterioration.

### 2.3.4 CNN-Based OCR with Neuro-Fuzzy Inference

**Anonymous (2022)** [4] combined a CNN-based OCR system with an **Adaptive Neuro-Fuzzy Inference System (ANFIS)** for medieval Tamil inscriptions. The ANFIS component was used to handle uncertain or ambiguous predictions from the CNN. While the results showed some improvement in handling edge cases, the added complexity of the neuro-fuzzy component made the system harder to deploy as a practical tool.

---

## 2.4 Recognition of Other Ancient Scripts

Researchers around the world have applied similar deep learning techniques to ancient scripts from other civilizations. Studying these efforts helps us understand the broader landscape of challenges and solutions in this field.

### 2.4.1 Ancient Kannada Inscription Recognition

**Anonymous (2023)** [8] developed a **hybrid CNN-RNN model** to read ancient Kannada inscriptions. The CNN layers were used for visual feature extraction from the character images, while the RNN (Recurrent Neural Network) layers were used to model sequential dependencies between characters in a word. Their model achieved an accuracy of 95% on their test set. This work demonstrated that combining spatial feature learning (CNN) with temporal sequence modeling (RNN) can be effective for epigraphical OCR. However, the Kannada script has fewer character variations than Vatteluttu, which may partly explain the higher accuracy.

### 2.4.2 Ashokan Brahmi Character Recognition

**Anonymous (2022)** [9] applied the **MobileNet architecture** — a lightweight deep learning model originally designed for mobile devices — to recognize characters from Ashokan Brahmi inscriptions. Brahmi is one of the oldest writing systems of the Indian subcontinent, dating back to the 3rd century BCE. The researchers used transfer learning (pre-training on a large general image dataset and then fine-tuning on Brahmi characters) to compensate for the small size of their training set. They achieved a validation accuracy of 95.94%. The success of the lightweight MobileNet architecture on this task suggests that ancient script recognition does not necessarily require extremely large and complex models — well-chosen architectures combined with transfer learning can deliver strong results.

### 2.4.3 Damaged Stone Inscription Processing

One of the most difficult challenges in epigraphical OCR is dealing with physical damage — missing strokes, cracks running through characters, and partially worn-away carvings. **Anonymous (2022)** [10] addressed this problem head-on by using **Stacked-UNet networks combined with Generative Adversarial Networks (GANs)**. Their approach first attempted to reconstruct the missing or damaged portions of each character before attempting recognition. The GAN component generated plausible completions of damaged characters based on patterns learned from intact examples. This is a promising direction, though it adds significant computational complexity.

### 2.4.4 InceptionV3 for Epigraphical Images

**Anonymous (2022)** [11] applied the **InceptionV3** deep learning architecture to epigraphical images. They introduced a preprocessing technique called **Seam Carving** — an algorithm originally designed for content-aware image resizing — to better isolate and separate characters before classification. The InceptionV3 model, with its multi-scale feature extraction capabilities, proved effective at handling the variability in character sizes found in real inscriptions.

### 2.4.5 Ancient Chinese Character Recognition

Moving beyond Indian scripts, **Anonymous (2023)** [12] worked on recognizing ancient Chinese characters using a modified version of the **Swin-Transformer** model. Transformers are a newer class of deep learning models that have shown remarkable success in natural language processing and are increasingly being applied to computer vision tasks. Their model used a **flexible data enhancement** strategy to improve robustness and achieved an accuracy of 87.25%. While this accuracy is lower than CNN-based approaches for simpler scripts, ancient Chinese has an enormous number of character classes (potentially thousands), making it one of the hardest character recognition problems in existence.

---

## 2.5 Image Preprocessing for Historical Documents

Before any character can be recognized by an AI model, the image must first be cleaned and prepared. The quality of preprocessing directly impacts the accuracy of everything that follows. Several studies have focused specifically on improving preprocessing techniques for historical and degraded documents.

### 2.5.1 Document Image Binarization

Binarization — the process of converting a grayscale image into a pure black-and-white image — is one of the most critical preprocessing steps. The goal is to separate the text (foreground) from the background as cleanly as possible.

**Anonymous (2024)** [14] published a comprehensive survey on **document image binarization** that reviewed dozens of different binarization methods. The survey found that **adaptive thresholding methods** (where the threshold value varies based on local image conditions) consistently outperform global thresholding methods (where a single threshold is applied to the entire image) when dealing with unevenly lit or degraded documents. Among adaptive methods, **Otsu's thresholding** was highlighted as a particularly reliable and widely used approach.

**Anonymous (2021)** [13] studied the impact of various **preprocessing methods on OCR performance** for digital historical documents. They tested combinations of noise filtering, binarization, deskewing, and contrast enhancement. Their key finding was that no single preprocessing step alone was sufficient — the best results came from carefully sequenced multi-step pipelines where each step built upon the improvements of the previous one. This finding directly influenced the design of VattalettuX's four-stage preprocessing pipeline.

### 2.5.2 CRF-Based Binarization

**Anonymous (2013)** [16] proposed a different approach to binarization using **Conditional Random Fields (CRF)** that exploited stroke orientation information. Instead of treating each pixel independently, the CRF approach modeled spatial relationships between neighbouring pixels, which helped preserve thin strokes that might otherwise be lost during standard binarization. While this approach showed good results on handwritten historical text, it was computationally more expensive than simpler adaptive thresholding methods.

### 2.5.3 Early OCR Preprocessing

**Gupta (2007)** [15] published early work on **OCR binarization and image pre-processing** specifically designed for searching within historical documents. This study laid some of the groundwork for modern approaches by demonstrating that thoughtful preprocessing could significantly improve the searchability and readability of digitized historical collections.

---

## 2.6 Convolutional Neural Networks for Image Classification

The AI backbone of VattalettuX is a Convolutional Neural Network (CNN). Understanding the evolution and capabilities of CNN architectures was essential for making informed design choices in this project.

### 2.6.1 Evolution of CNN Architectures

**Anonymous (2023)** [17] published a survey titled "Advancements and Challenges in Character Recognition: A Comparative Analysis of CNN and Deep Learning Approaches." This survey traced the evolution of CNN architectures from early designs like **LeNet** (1998) — which had just a few layers and could only handle simple digit recognition — all the way to modern architectures like **ResNet** (2015), **InceptionNet** (2014), and **EfficientNet** (2019). The key insight from this evolution is that deeper networks (with more layers) generally perform better, but only if they include mechanisms like **skip connections** (used in ResNet) to prevent the "vanishing gradient" problem.

**Anonymous (2023)** [18] published another comprehensive survey titled "Convolutional Neural Networks: A Survey," covering the mathematical foundations, architectural innovations, training strategies, and real-world applications of CNNs across various domains. This survey strongly influenced our decision to use a ResNet-inspired architecture for VattalettuX, given ResNet's proven track record on large-scale image classification tasks.

### 2.6.2 Image Classification with CNNs

**Anonymous (2022)** [19] reviewed image classification algorithms based on CNNs. Their analysis confirmed that CNNs remain the gold standard for image classification tasks, particularly when the number of classes is large and the visual differences between classes are subtle — both of which apply to Vatteluttu character recognition.

**Anonymous (2021)** [20] developed a "Full-depth CNN Classifier" for handwritten and license plate character recognition. Their work demonstrated that deeper CNN architectures with carefully tuned dropout and regularization could achieve excellent accuracy on multi-class character recognition tasks, even when the training dataset was relatively small. The dropout and regularization strategies they described were directly relevant to our model design.

---

## 2.7 Data Augmentation and Transfer Learning

When labeled training data is scarce — as it is for almost all ancient scripts — two techniques become especially important: data augmentation and transfer learning.

### 2.7.1 Data Augmentation

**Anonymous (2023)** [21] conducted a comprehensive survey on **data augmentation for handwritten character recognition**. They catalogued dozens of augmentation techniques, including geometric transformations (rotation, scaling, shearing), photometric transformations (brightness, contrast, noise addition), and more advanced methods like elastic deformation and random erasing. Their findings showed that data augmentation can improve model accuracy by 5-15% in data-scarce scenarios — a significant margin.

**Anonymous (2022)** [22] explored the use of **conditional GANs (Generative Adversarial Networks)** for **synthetic data generation** in few-shot handwritten character recognition. GANs can generate entirely new, realistic-looking character images that the model has never seen before, effectively expanding the training set. While we did not use GANs in VattalettuX, the concept of synthetic data generation influenced our approach of programmatically generating 1,000 variations of each character from authentic font resources.

### 2.7.2 Transfer Learning

**Anonymous (2022)** [23] surveyed the use of **deep learning for historical document analysis and recognition**. They highlighted transfer learning as a critical enabler for historical document OCR, since most historical scripts lack the millions of labeled images that modern deep learning models typically require. Transfer learning allows a model pre-trained on a large general-purpose dataset (like ImageNet) to be fine-tuned on a much smaller domain-specific dataset.

**Anonymous (2022)** [24] specifically studied **transfer learning with ResNet and VGG** architectures for historical document image classification. They found that ResNet-based transfer learning consistently outperformed VGG-based approaches, likely because ResNet's skip connections help preserve useful low-level features during fine-tuning. This finding further supported our choice of ResNet as the base architecture for VattalettuX.

---

## 2.8 Summary of Literature Review

The following table summarizes the key studies reviewed in this chapter:

| # | Study | Script / Domain | Method | Classes | Accuracy | Key Contribution |
|---|-------|----------------|--------|---------|----------|-----------------|
| 1 | Vijaya Arjunan et al. (2025) [1] | Vatteluttu | Siamese CNN-RNN | 28 | 98.0% | First dedicated Vatteluttu OCR |
| 2 | Anonymous (2023) [2] | Ancient Tamil | RCNN | - | 98.6% | Recognition from artifacts |
| 3 | Anonymous (2022) [3] | Medieval Tamil | 2D-CNN + TTS | - | 77.7% | Text-to-speech integration |
| 4 | Anonymous (2022) [4] | Medieval Tamil | CNN + ANFIS | - | - | Neuro-fuzzy post-processing |
| 5 | Anonymous (2022) [5] | Tamil Palm Leaf | CNN | - | - | Morphological preprocessing |
| 6 | Anonymous (2022) [6] | Tamil Palm Leaf | Deep Learning | - | - | Cursive character handling |
| 7 | Anonymous (2023) [7] | Tamil Palm Leaf | Deep Learning | - | - | Noise reduction filters |
| 8 | Anonymous (2023) [8] | Kannada | CNN-RNN Hybrid | - | 95.0% | Sequence modeling for epigraphy |
| 9 | Anonymous (2022) [9] | Brahmi | MobileNet | - | 95.94% | Lightweight architecture + TL |
| 10 | Anonymous (2022) [10] | Damaged Inscriptions | Stacked-UNet + GAN | - | - | Character reconstruction |
| 11 | Anonymous (2022) [11] | Epigraphy | InceptionV3 | - | - | Seam Carving preprocessing |
| 12 | Anonymous (2023) [12] | Ancient Chinese | Swin-Transformer | - | 87.25% | Transformer for ancient OCR |

---

## 2.9 Gaps Identified in Existing Research

Based on our thorough review of the existing literature, we identified the following key gaps that VattalettuX aims to address:

1. **Limited Character Coverage**: The only published study on Vatteluttu OCR [1] covered just 28 out of 247 characters. No system exists that can handle the complete Vatteluttu character set as defined by Tamil grammar.

2. **No Deployed System**: While several studies reported good laboratory accuracy, none of them resulted in a publicly accessible, deployed application that an end user can actually use. VattalettuX includes a fully functional web application.

3. **No Modern Tamil Mapping**: Previous studies treated the problem as a pure classification task — recognizing which Vatteluttu character is present in an image. None of them included the crucial step of mapping the recognized character to its Modern Tamil equivalent, which is essential for making the results useful to non-expert users.

4. **No End-to-End Pipeline**: Most prior studies focused on either preprocessing, segmentation, or classification in isolation. VattalettuX integrates all four stages (preprocessing, segmentation, classification, and mapping) into a single, seamless pipeline.

5. **No Recognition History**: None of the previous systems provided any mechanism for storing and retrieving past recognition sessions. VattalettuX includes a MySQL-backed history feature that allows users to review all their previous recognition results.

6. **Limited Preprocessing for Stone Surfaces**: While several studies applied preprocessing to palm leaf manuscripts or printed historical documents, very few designed preprocessing pipelines specifically optimized for the unique noise characteristics of stone inscriptions (shadows, surface cracks, moss, uneven carving depths).

These gaps collectively justify the development of VattalettuX as a meaningful contribution to the field of ancient script recognition and Tamil cultural heritage preservation.

---
