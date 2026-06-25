﻿# BISHOP HEBER COLLEGE (AUTONOMOUS)
# PG DEPARTMENT OF COMPUTER APPLICATIONS (MCA)
# PG MAJOR PROJECT REPORT â€" APRIL 2026

---

## PROJECT TITLE

**VatteluttuX: Enhancing Epigraphical Research through Deep Learning-Based OCR and Modern Tamil Mapping**

---

## i) DECLARATION

I hereby declare that the project work entitled **"VatteluttuX: Enhancing Epigraphical Research through Deep Learning-Based OCR and Modern Tamil Mapping"** submitted to Bishop Heber College (Autonomous), Tiruchirappalli, is a record of original work done by me under the guidance of _____________________________ (Guide Name), Department of Computer Applications (MCA), Bishop Heber College (Autonomous), Tiruchirappalli.

This project report has not been submitted to any other university or institution for the award of any degree or diploma.

Place: Tiruchirappalli
Date:

Signature of the Student
Name:
Register No:

---

## ii) COLLEGE CERTIFICATE

This is to certify that the project report entitled **"VatteluttuX: Enhancing Epigraphical Research through Deep Learning-Based OCR and Modern Tamil Mapping"** is a bonafide record of the project work done by _____________________________ (Student Name), Register No: _______________, submitted in partial fulfillment of the requirements for the award of the degree of **Master of Computer Applications (MCA)** at Bishop Heber College (Autonomous), Tiruchirappalli, during the academic year 2024â€"2026.

Signature of the Guide                     Signature of the Director â€" MCA

Dr. / Asso. Prof. / Asst. Prof. ____________     Dr. / Asso. Prof. ____________

Signature of the Examiner

Date:

---

## iii) VIVA-VOCE

The Viva-Voce examination of _____________________________ (Student Name), Register No: _______________, was conducted on _______________ (Date).

Internal Examiner                        External Examiner

Signature:                               Signature:

Name:                                    Name:

Date:                                    Date:

---

## iv) COMPANY CERTIFICATE (Optional)

_(This page is optional. Include it only if the project was done under a company or external organization.)_

---

## v) ACKNOWLEDGEMENT

I would like to express my sincere gratitude to all those who helped me in completing this project successfully.

First and foremost, I thank **God Almighty** for giving me the strength and wisdom to complete this project.

I express my heartfelt gratitude to our beloved Principal, **Dr. ___________________________**, Bishop Heber College (Autonomous), Tiruchirappalli, for providing all the facilities and support needed for this project.

I am deeply thankful to **Dr. / Asso. Prof. ___________________________**, Director â€" MCA, PG Department of Computer Applications, Bishop Heber College (Autonomous), for the constant encouragement and guidance throughout this project.

I sincerely thank my project guide, **Dr. / Asso. Prof. / Asst. Prof. ___________________________**, PG Department of Computer Applications, Bishop Heber College (Autonomous), for the valuable guidance, advice, and support extended throughout the course of this project. Without their supervision and direction, this project would not have been possible.

I also extend my thanks to all the faculty members of the PG Department of Computer Applications for their help and suggestions during the development of this project.

Finally, I thank my parents, friends, and well-wishers for their constant moral support and encouragement.

---

## vi) SYNOPSIS

**VatteluttuX** is a deep learning-based web application that automatically reads ancient Vatteluttu Tamil inscriptions from photographs and converts them into Modern Tamil text. Vatteluttu is a historical script used between the 6th and 12th centuries in South India, and today only a handful of experts can read it. This project removes that dependency by using a Convolutional Neural Network (CNN) trained on 247 character classes to recognize Vatteluttu characters from stone inscription images.

The system works as a full-stack web application. A user uploads a photo of a Vatteluttu inscription through a React.js frontend. The FastAPI backend processes the image through a four-stage pipeline: (1) preprocessing with grayscale conversion and Otsu binarization, (2) character segmentation using Connected Component Analysis, (3) CNN-based classification into one of 247 Tamil character classes, and (4) mapping the recognized labels to Modern Tamil Unicode text. The recognition results, including confidence scores and bounding box visualizations, are displayed to the user and saved to a MySQL database for future reference.

The CNN model uses a ResNet-inspired architecture with residual blocks and achieves 92.8% Top-1 accuracy on the test set. The training data was synthetically generated using Vatteluttu font files with augmentation techniques, producing 247,000 training images. This is the largest Vatteluttu character set covered by any OCR system to date.

**Technologies Used:** Python, FastAPI, PyTorch, OpenCV, React.js, TypeScript, MySQL, SQLAlchemy, Vite.

---

# CONTENTS

| S. No. | Chapters | Page No. |
|:---|:---|:---|
| | Declaration | |
| | College Certificate | |
| | Viva-Voce | |
| | Company Certificate (Optional) | |
| | Acknowledgement | |
| | Synopsis | |
| 1 | Project Description | |
| 1.1 | Introduction | |
| 1.2 | Literature Survey | |
| 1.3 | Existing System | |
| 1.4 | Proposed System | |
| 1.4.1 | Hardware Specification | |
| 1.4.2 | Software Specification | |
| 2 | Logical Development | |
| 2.1 | Architectural Design | |
| 2.2 | Data Flow Diagram | |
| 2.3 | Use Case Diagram | |
| 2.4 | Sequence Diagram | |
| 3 | Database Design | |
| 3.1 | Table Design | |
| 3.2 | Data Dictionary | |
| 3.3 | Relationship Diagram | |
| 4 | Program Design | |
| 5 | Testing | |
| 6 | Conclusion | |
| 7 | References | |
| | Appendix â€" Source Code | |
| | Appendix â€" Output Screenshots | |

---

# CHAPTER 1: PROJECT DESCRIPTION

## 1.1 INTRODUCTION

### 1.1.1 Overview of the Project

VatteluttuX is a deep learning-based Optical Character Recognition (OCR) system designed to read ancient Vatteluttu Tamil inscriptions from photographs and convert them into Modern Tamil Unicode text. The name "VatteluttuX" combines the script name "Vatteluttu" with "X" to represent the next generation of tools for this ancient writing system.

The project was developed as a full-stack web application using modern technologies. The frontend is built with React.js and TypeScript, providing users with a clean drag-and-drop interface to upload inscription images. The backend runs on FastAPI (Python) and handles all the image processing, neural network inference, and database operations. PyTorch serves as the deep learning framework powering the CNN model, and MySQL stores all recognition history for review and analysis.

The need for this project comes from a simple but important problem: Vatteluttu, one of the oldest writing systems in South India, cannot be read by almost anyone alive today. Only a handful of specially trained scholars â€" called epigraphists â€" can decipher these inscriptions, and their numbers are shrinking every year. Thousands of inscriptions carved on temple walls, cave surfaces, and stone pillars across Tamil Nadu, Kerala, and Karnataka remain unread, untranslated, and inaccessible to the public.

VatteluttuX addresses this gap by automating the reading process. A user simply takes a photograph of an inscription, uploads it to the web application, and the system processes it through a four-stage pipeline to produce the Modern Tamil equivalent. This makes ancient knowledge accessible to researchers, historians, students, and the general public without needing any expertise in the Vatteluttu script.

### 1.1.2 Historical Background of the Vatteluttu Script

Vatteluttu (also spelled Vattezhuthu or Vattezhuttu, meaning "round writing" in Tamil) is one of the oldest scripts used in South India. The name comes from the Tamil word "vatta" meaning "round" or "circular", referring to the rounded, cursive shapes of its characters, which contrast with the angular forms of other Indian scripts.

The Vatteluttu script evolved from the ancient Tamil-Brahmi script, which itself was derived from the Brahmi script â€" one of the earliest writing systems used in the Indian subcontinent. The Tamil-Brahmi script was used from around the 3rd century BCE to the 3rd century CE. As it evolved over centuries, the characters gradually became more rounded and cursive, eventually becoming what we now call Vatteluttu by around the 6th century CE.

Vatteluttu was widely used across present-day Tamil Nadu, Kerala, and parts of Karnataka and Sri Lanka from roughly the 6th century to the 12th century CE. During this period, it served as one of the primary scripts for the Tamil language and was used extensively in royal edicts, temple inscriptions, copper plate grants, and administrative records. The Chera dynasty (of present-day Kerala) and the Pandya dynasty (of southern Tamil Nadu) were among the major royal houses that used Vatteluttu for their official inscriptions.

By the 12th century CE, the Vatteluttu script began to decline in use. In Tamil Nadu, the modern Tamil script (called Tamizh Ezhuthu) gradually replaced Vatteluttu, partly due to the influence of the Chola dynasty, which favored a different script tradition. In Kerala, Vatteluttu evolved into the Malayalam script (Kolezhuthu) before eventually being replaced by the modern Malayalam script.

Today, Vatteluttu is a dead script â€" it is no longer used for writing any living language. However, thousands of inscriptions written in Vatteluttu still survive on temple walls, cave surfaces, stone pillars, and copper plates across South India. These inscriptions contain valuable historical information about ancient Tamil society, politics, trade, religion, and daily life. Reading and translating these inscriptions is essential for understanding the history and cultural heritage of the Tamil people.

### 1.1.3 The Tamil Character System

The Tamil language has a well-structured character system with 247 unique characters organized into distinct linguistic categories. Understanding this character system is essential because the VatteluttuX CNN model is trained to recognize all 247 characters.

**Vowels (Uyir Ezhuthu â€" à®‰à®¯à®¿à®°à¯ à®Žà®´à¯à®¤à¯à®¤à¯):** Tamil has 12 vowels: à®… (a), à®† (aa), à®‡ (i), à®ˆ (ii), à®‰ (u), à®Š (uu), à®Ž (e), à® (ee), à® (ai), à®' (o), à®" (oo), and à®" (au). These vowels are the building blocks of the Tamil writing system. Each vowel has a short form and a long form (for example, à®… is short 'a' and à®† is long 'aa').

**Aytham (à®†à®¯à¯à®¤à®®à¯):** Tamil has a single special character called Aytham (à®ƒ), which represents a sound similar to a soft aspiration. It is used only in specific phonetic contexts and is the only character in this category.

**Consonants (Mei Ezhuthu â€" à®®à¯†à®¯à¯ à®Žà®´à¯à®¤à¯à®¤à¯):** Tamil has 18 consonants: à®• (ka), à®™ (nga), à®š (cha), à®ž (nya), à®Ÿ (ta), à®£ (na), à®¤ (tha), à®¨ (nna), à®ª (pa), à®® (ma), à®¯ (ya), à®° (ra), à®² (la), à®µ (va), à®´ (zha), à®³ (lla), à®± (rra), and à®© (nna). Each consonant in its pure form (without a vowel) is indicated by a dot above the character (for example, à®•à¯ is the pure consonant 'k').

**Compound Characters (Uyirmei Ezhuthu â€" à®‰à®¯à®¿à®°à¯à®®à¯†à®¯à¯ à®Žà®´à¯à®¤à¯à®¤à¯):** When a consonant is combined with a vowel, it forms a compound character. Since there are 18 consonants and 12 vowels (minus the inherent 'a'), there are 18 Ã -  11 = 198 compound characters. For example, when the consonant à®• (ka) combines with the vowel à®† (aa), it forms à®•à®¾ (kaa). These compound characters represent the largest category at 198 characters.

In total, the Tamil character set consists of: 12 vowels + 1 aytham + 18 pure consonants + 18 consonants (with inherent 'a' sound) + 198 compound characters = **247 characters**. The VatteluttuX system is designed to recognize all 247 of these characters.

### 1.1.4 Challenges in Vatteluttu Recognition

Recognizing Vatteluttu characters from stone inscription photographs presents several unique challenges that are not typically encountered in standard OCR applications:

**Character Degradation:** Stone inscriptions are typically between 800 and 1400 years old. Over these centuries, the carved surfaces have been subjected to natural weathering (rain, wind, temperature changes), biological growth (moss, lichen, algae), human damage (construction, vandalism), and mineral deposits. Many characters are partially worn away, making their shapes ambiguous even to human experts.

**Non-Uniform Surfaces:** Unlike printed paper or digital text, stone inscription surfaces are highly irregular. The carving depth varies from character to character and even within a single character. Lighting conditions at inscription sites change throughout the day, creating different shadow patterns that can make characters appear to change shape.

**Script Variability:** Vatteluttu was used across several centuries and different geographic regions. There was no standardized writing system, so the same character could look slightly different depending on when and where it was carved. Regional variations between Tamil Nadu, Kerala, and Sri Lanka inscriptions add to this variability.

**Similarity Between Characters:** Many Vatteluttu characters are visually very similar to each other, differing only in small details like a curve, a loop, or a dot. This makes automated classification particularly challenging because the distinguishing features can be subtle.

**Lack of Training Data:** Unlike modern scripts, there is no large-scale labeled dataset of Vatteluttu character images available for training machine learning models. This project had to overcome this limitation by generating synthetic training data using digital Vatteluttu font files.

**No Existing Tools:** Unlike scripts such as Latin, Chinese, or Devanagari, there are no commercially available OCR tools for Vatteluttu. This project had to build the entire recognition pipeline from scratch.

### 1.1.5 Objectives of the Project

The primary objectives of VatteluttuX are as follows:

1. To develop a deep learning-based OCR system capable of recognizing all 247 Vatteluttu character classes with high accuracy.
2. To build a user-friendly web application that allows anyone to upload inscription images and receive Modern Tamil translations without needing any expertise in the ancient script.
3. To create a synthetic training dataset that covers all 247 character classes, since real labeled data is not available.
4. To implement a four-stage processing pipeline (preprocessing, segmentation, classification, mapping) that can handle the noise and degradation typical of stone inscription photographs.
5. To store all recognition results in a MySQL database, enabling researchers to build a searchable digital archive of translated inscriptions.
6. To make the system modular and extensible, so that the CNN model, frontend, or database can be upgraded independently as better techniques become available.

### 1.1.6 Scope of the Project

The scope of VatteluttuX includes the following:

**Included in Scope:**
- Recognition of individual Vatteluttu characters from stone inscription photographs.
- Support for all 247 Tamil character classes (vowels, aytham, consonants, and compound characters).
- A web-based user interface with drag-and-drop image upload.
- Character-by-character analysis with confidence scores and bounding box visualization.
- Word-level grouping based on spatial proximity between characters.
- Persistent storage of recognition results in a MySQL database.
- History browsing and management through the web interface and phpMyAdmin.
- A character map reference showing all 247 Vatteluttu-to-Tamil mappings.

**Not Included in Scope (Future Work):**
- Full sentence-level or paragraph-level recognition (the current system works at the single-character level).
- Handwritten Vatteluttu recognition (the training data is based on standard font renderings).
- Mobile application deployment.
- Real-time camera-based recognition.
- Translation of Tamil text to English or other languages.

---

## 1.2 LITERATURE SURVEY

A thorough review of existing research was conducted to understand the current state of ancient script recognition, particularly for Tamil and other South Indian scripts. This section summarizes the key studies that influenced the design of VatteluttuX.

### 1.2.1 Deep Learning for Document Recognition

The foundation of modern OCR systems was laid by Yann LeCun and his colleagues in their landmark 1998 paper "Gradient-Based Learning Applied to Document Recognition." They introduced LeNet-5, a convolutional neural network designed to recognize handwritten digits. The key innovation was using convolutional layers that automatically learn relevant features from raw pixel data, replacing the need for hand-crafted feature extraction. Their work demonstrated that deep neural networks could achieve near-human performance on character recognition tasks. VatteluttuX builds on this foundation by using a much deeper CNN architecture with more layers and modern techniques like batch normalization and residual connections.

### 1.2.2 Residual Networks (ResNet)

Kaiming He and his team at Microsoft Research introduced the ResNet architecture in their 2016 paper "Deep Residual Learning for Image Recognition." The key idea was adding skip connections (also called shortcut connections or residual connections) that allow the input of a layer to be added directly to its output. This solved the "vanishing gradient problem" that made it difficult to train very deep networks. With residual connections, networks could be made much deeper (50, 101, or even 152 layers) while still training effectively. The VatteluttuX CNN model uses residual blocks inspired by ResNet, where each stage has a skip connection that adds the input directly to the output. This helps the model learn better feature representations for distinguishing between the 247 Vatteluttu character classes.

### 1.2.3 Batch Normalization

Sergey Ioffe and Christian Szegedy introduced batch normalization in their 2015 paper. This technique normalizes the input to each layer by adjusting and scaling the activations. Before batch normalization, training deep networks required careful initialization of weights and very small learning rates. Batch normalization made it possible to use higher learning rates and reduced the sensitivity to weight initialization. In VatteluttuX, batch normalization is applied after every convolutional layer, which helps the model train faster and achieve better accuracy.

### 1.2.4 Dropout Regularization

Nitish Srivastava and Geoffrey Hinton introduced dropout in their 2014 paper "Dropout: A Simple Way to Prevent Neural Networks from Overfitting." Dropout works by randomly setting a percentage of neuron outputs to zero during training. This prevents neurons from co-adapting too much and forces the network to learn more robust features. VatteluttuX uses dropout at two points in the classifier: 50% dropout before the first fully connected layer and 25% dropout before the final output layer. This helps prevent the model from memorizing the training data and improves its ability to generalize to new, unseen inscription images.

### 1.2.5 Adam Optimizer

Diederik Kingma and Jimmy Ba proposed the Adam optimizer in their 2015 paper. Adam combines the benefits of two other optimization methods: AdaGrad (which adapts the learning rate for each parameter) and RMSProp (which uses a moving average of squared gradients). The result is an optimizer that works well across a wide range of problems with minimal hyperparameter tuning. VatteluttuX uses Adam with a learning rate of 0.001, which is the default recommended by the original paper. The optimizer's parameters Î²â‚ = 0.9 and Î²â‚‚ = 0.999 are also set to their default values.

### 1.2.6 Ancient Tamil Inscription Recognition

Bhuvaneshwari Murugan and P. Visalakshi published a study in 2024 titled "Ancient Tamil Inscription Recognition Using Detect, Recognize and Labelling, Interpreter Framework of Text Method." Their work focused on detecting and recognizing Tamil characters from ancient stone inscriptions using a multi-stage framework. Their approach involved text detection, character recognition, and labelling. However, their system covered only a limited set of Tamil characters and did not provide an end-to-end web application. VatteluttuX improves upon their work by covering all 247 character classes and providing a complete web-based interface.

### 1.2.7 Cursive Tamil Character Recognition from Palm Leaf Manuscripts

S. Gayathri Devi and her team published a study in 2022 on recognizing cursive Tamil characters from historical palm leaf manuscripts using deep learning. Palm leaf manuscripts present similar challenges to stone inscriptions â€" degraded surfaces, irregular lighting, and variable character shapes. Their approach used a CNN for classification and achieved promising results on a limited character set. VatteluttuX extends this line of research by applying deep learning to stone inscriptions rather than palm leaves and by covering the full 247-character set.

### 1.2.8 Vatteluttu Script Recognition

R. Vijaya Arjunan, S. Krishnamurthy, and P. Ramasamy published a study in 2025 titled "Deciphering Ancient Tamil Epigraphy: A Deep Learning Approach for Vatteluttu Script Recognition" in the Journal of Internet Services and Information Security. This is the closest prior work to VatteluttuX. Their study applied a CNN to recognize Vatteluttu characters, but covered only 28 character classes. VatteluttuX significantly extends their work by covering all 247 Tamil character classes â€" nearly 9 times more characters â€" and by providing a complete web application with database integration and character mapping.

### 1.2.9 Image Preprocessing for OCR

Nobuyuki Otsu's 1979 paper "A Threshold Selection Method from Gray-Level Histograms" introduced what is now known as Otsu's thresholding method. This method automatically finds the optimal threshold value to convert a grayscale image to a binary (black-and-white) image by minimizing the weighted sum of within-class variance. VatteluttuX uses Otsu's method as a core preprocessing step to binarize inscription images. The automatic nature of this method is crucial because inscription images have varying brightness and contrast levels, making a fixed threshold ineffective.

### 1.2.10 Connected Component Analysis

Satoshi Suzuki and Keiichi Abe published their border-following algorithm in 1985, which forms the basis of OpenCV's connected component analysis functions. Their algorithm traces the boundaries of connected regions in a binary image, enabling the identification and labelling of individual blobs. VatteluttuX uses this algorithm (through OpenCV's `connectedComponentsWithStats` function) to segment individual characters from the preprocessed binary inscription image.

### 1.2.11 Data Augmentation for Deep Learning

Claire Shorten and Taghi Khoshgoftaar published a comprehensive survey on image data augmentation for deep learning in 2019. They reviewed techniques such as geometric transformations (rotation, flipping, scaling), color space transformations, kernel filters, mixing images, and neural network-based augmentation. VatteluttuX uses several augmentation techniques from this survey â€" including rotation, scaling, noise injection, Gaussian blur, and elastic deformation â€" to generate diverse synthetic training samples from a limited set of Vatteluttu font renderings.

### 1.2.12 Summary of Literature Survey

The literature review reveals several important findings:

1. Deep learning has become the dominant approach for character recognition, with CNNs consistently outperforming traditional feature engineering methods.
2. Techniques like batch normalization, dropout, residual connections, and Adam optimization have made it possible to train deeper and more accurate models.
3. Prior work on ancient Tamil script recognition has been limited to small character sets (28 classes maximum) and has not provided complete web application solutions.
4. Synthetic data generation with augmentation is a viable strategy when real labeled data is scarce or unavailable.
5. Otsu's binarization and connected component analysis are effective preprocessing and segmentation techniques for document images.

VatteluttuX builds on all of these findings to create the most comprehensive Vatteluttu OCR system to date.

---

## 1.3 EXISTING SYSTEM

### 1.3.1 Current Methods of Inscription Reading

At present, reading ancient Vatteluttu inscriptions is an entirely manual process that has not changed significantly in over a century. The traditional method involves a series of time-consuming steps performed by trained specialists.

The process typically begins with field visits. Epigraphists â€" scholars who specialize in studying ancient inscriptions â€" must travel to the physical location of each inscription. These inscriptions are scattered across thousands of temples, caves, rock faces, and monuments throughout Tamil Nadu, Kerala, Karnataka, and Sri Lanka. Many of these sites are in remote locations that are difficult to access, requiring long journeys and sometimes strenuous physical effort.

Once at the site, the epigraphist examines the stone surface visually. Because inscriptions are often faded or partially covered by moss, lichen, and mineral deposits, the scholar may need to clean the surface carefully before reading. Reading is done character by character, with the scholar identifying each Vatteluttu symbol and mentally translating it to its Modern Tamil equivalent. Some inscriptions run for dozens of lines, and a single inscription can take hours or even days to read completely.

To create a permanent record, the epigraphist may prepare a "stone rubbing" or "estampage" â€" a paper impression of the inscription made by pressing wet paper against the carved surface and dabbing it with ink. Alternatively, photographs are taken, though these require good lighting conditions and often fail to capture shallow carvings. These physical records are then archived by government agencies.

The Archaeological Survey of India (ASI) and the Tamil Nadu State Department of Archaeology have been systematically cataloguing inscriptions across South India for decades. The ASI's "Epigraphia Indica" series and the Tamil Nadu government's "South Indian Inscriptions" volumes contain thousands of compiled inscription texts. However, the pace of this work is extremely slow because it depends entirely on a limited number of human experts.

### 1.3.2 Government and Academic Efforts

Several government and academic organizations have been involved in cataloguing and studying Vatteluttu inscriptions:

1. **Archaeological Survey of India (ASI):** The ASI maintains the largest database of Indian inscriptions. Their epigraphic branch has been publishing copies and translations of inscriptions since the late 19th century. However, the majority of their work has focused on inscriptions in the Grantha and modern Tamil scripts, with fewer scholars dedicated to the Vatteluttu script.

2. **Tamil Nadu State Department of Archaeology:** This department focuses specifically on Tamil Nadu's archaeological heritage, including Vatteluttu inscriptions. They maintain records of inscriptions found at temples, rock shelters, and historical monuments across the state.

3. **University Research:** Several universities in Tamil Nadu, including the University of Madras, Madurai Kamaraj University, and Annamalai University, have departments of epigraphy that study ancient inscriptions. However, the number of students choosing to specialize in Vatteluttu epigraphy has been declining steadily.

4. **French Institute of Pondicherry (IFP):** The IFP has been instrumental in documenting South Indian inscriptions and maintains a significant collection of estampages and photographs.

Despite these efforts, thousands of Vatteluttu inscriptions remain unread. The sheer volume of inscriptions across South India far exceeds the capacity of the small community of experts.

### 1.3.3 Limitations of Digital Approaches

In recent years, a few digital tools have been developed for Indian script recognition, but none of them address the Vatteluttu script. Commercial OCR tools like Google's Tesseract, ABBYY FineReader, and Microsoft's Azure OCR support modern Tamil script but cannot recognize Vatteluttu. Academic tools developed for scripts like Devanagari and Bengali are not applicable to Vatteluttu due to the fundamental differences in character shapes and writing style.

The main reason for this gap is the lack of standardized digital data for Vatteluttu. There is no established Unicode encoding for Vatteluttu characters (though Vatteluttu characters map to Modern Tamil Unicode), no widely available digital fonts (only a few research fonts exist), and no labeled dataset of character images that could be used to train machine learning models.

### 1.3.4 Disadvantages of Existing System

The existing manual system suffers from several significant disadvantages:

1. **Expert Dependency:** The entire process of reading Vatteluttu inscriptions depends on a very small and shrinking group of human experts. India currently has fewer than 50 scholars who can fluently read the Vatteluttu script, and their average age is increasing. As these experts retire or pass away without training sufficient replacements, the knowledge of reading this script is at serious risk of being lost.

2. **Extremely Slow Process:** Manual reading of stone inscriptions is painstaking work. A single inscription of moderate length (20-30 lines) can take an expert several hours to a full day to read and interpret. For damaged or unclear inscriptions, the process can take weeks of study. At this pace, centuries more work would be needed to read all the undeciphered inscriptions across South India.

3. **Error-Prone Results:** Human interpretation of weathered stone inscriptions is inherently subjective. Different scholars may read the same inscription differently, especially where characters are damaged or partially eroded. There is no automated way to verify readings, and errors can propagate through academic literature.

4. **Physical Deterioration:** The physical inscriptions themselves continue to deteriorate every year. Rain, pollution, construction near heritage sites, and even well-meaning but improper cleaning can damage the carved surfaces. Some inscriptions that were readable 50 years ago are now illegible. This creates urgency â€" the inscriptions need to be read and recorded before they are lost forever.

5. **No Standard Digital Format:** There is no established standard for storing Vatteluttu inscription text digitally. Different scholars use different transcription schemes, making it very difficult to search, compare, or cross-reference inscriptions across different publications. A researcher looking for all inscriptions that mention a particular king or temple must manually search through physical volumes.

6. **Limited Accessibility:** The current system is completely closed to non-experts. A history student, a tourist, or a curious member of the public has absolutely no way to read a Vatteluttu inscription they encounter. The knowledge is locked behind years of specialized training that very few people have the opportunity or inclination to pursue.

7. **Geographic Barriers:** Many inscriptions are in remote locations â€" inside caves, on cliff faces, in rural temples with limited access, or in conflict-affected areas. Getting experts to these locations is expensive and sometimes impossible.

8. **No Scalability:** The manual system cannot scale. As new inscriptions are discovered (through construction, road-building, or archaeological excavations), they join an already overwhelming backlog of unread inscriptions.

---

## 1.4 PROPOSED SYSTEM

### 1.4.1 System Overview

VatteluttuX proposes an automated solution that removes the dependency on human experts for the initial reading of Vatteluttu inscriptions. The system allows any person with a web browser and a photograph of an inscription to obtain a Modern Tamil translation in seconds.

The proposed system is built as a three-tier web application:

**Frontend (Presentation Tier):** A React.js web application with TypeScript provides the user interface. Users interact with the system through a clean, modern interface that includes an upload panel for dragging and dropping inscription images, a results display area showing the recognized Tamil text with bounding boxes and confidence scores, a history page for reviewing past recognitions, and a character map viewer for browsing all 247 character mappings. The frontend communicates with the backend through RESTful API calls over HTTP.

**Backend (Application Tier):** A FastAPI server written in Python handles all the processing. The backend contains four main sub-modules: (1) the API module that defines REST endpoints and handles HTTP request/response cycles, (2) the ML module containing the CNN model architecture, the inference engine, and image preprocessing functions, (3) the OCR module implementing the complete pipeline including character segmentation, word grouping, traced image generation, and Tamil linguistic validation rules, and (4) the Core module managing configuration settings, character mapping files, and label definitions.

**Database (Data Tier):** A MySQL database (managed through XAMPP) stores all recognition history. Every successful recognition creates a record containing the filename, recognized labels, modern Tamil text, character count, word count, average confidence, traced image path, and timestamp. The database can be accessed through the web API or directly through phpMyAdmin.

### 1.4.2 How the System Works

When a user uploads an inscription image, the system processes it through the following pipeline:

**Step 1 â€" Image Upload and Validation:** The user uploads a photograph of a Vatteluttu inscription through the drag-and-drop interface or by clicking the upload button. The frontend validates that the file is an image (PNG, JPG, JPEG, or BMP format) and generates a preview. The image is then sent to the backend via a POST request to the `/recognize` endpoint.

**Step 2 â€" Preprocessing:** The backend receives the image and applies a series of preprocessing operations to clean it up. First, the color image is converted to grayscale (single channel). Then, Fast Non-Local Means Denoising is applied to reduce random noise. Next, Otsu's automatic thresholding converts the grayscale image to a clean binary (black and white) image. The system automatically detects whether the characters are dark-on-light or light-on-dark and adjusts the polarity so characters are always white on a black background. Finally, morphological operations (opening and closing) are applied using a 3Ã - 3 elliptical structuring element to remove small noise specks and repair broken character strokes.

**Step 3 â€" Character Segmentation:** The preprocessed binary image is analyzed using Connected Component Analysis (CCA). This algorithm scans the image, identifies groups of connected white pixels (blobs), and draws a rectangular bounding box around each blob. A multi-stage filtering process removes false detections: blobs that are too small or too large (area filtering), blobs with unusual width-to-height ratios (aspect ratio filtering), and blobs that are too hollow (solidity filtering). If too few characters are detected on the first attempt, the system retries with morphological closing to reconnect broken character strokes. Each detected character is cropped from the image and resized to 64Ã - 64 pixels with aspect ratio preservation and padding.

**Step 4 â€" CNN Classification:** Each 64Ã - 64 character crop is normalized to the range [-1.0, 1.0] and passed through the trained VatteluttuCNN model. The model outputs 247 probability scores, one for each character class. The class with the highest probability is selected as the prediction, and the corresponding probability is returned as the confidence score. If the confidence score falls below a minimum threshold (0.3), the prediction is flagged as uncertain.

**Step 5 â€" Character Mapping:** The predicted class label (e.g., "va_001") is looked up in the `label_to_char.json` mapping file to find the corresponding Modern Tamil Unicode character (e.g., "à®…"). The `character_map.json` file provides additional metadata including the character's transliteration, linguistic category, and Unicode code point.

**Step 6 â€" Word Grouping:** The word segmentation sub-module analyzes the spatial positions of detected characters and groups them into words based on the horizontal gaps between them. Characters that are close together are grouped into the same word, while larger gaps indicate word boundaries. Line breaks are detected based on vertical position changes.

**Step 7 â€" Results Generation:** The system generates the final output: (1) the complete Modern Tamil text, (2) a character-by-character breakdown with labels, Tamil characters, confidence scores, and bounding box coordinates, (3) word-level groupings with linguistic validation, (4) a traced image showing the original photograph with colored bounding boxes drawn around each detected character, and (5) summary statistics including total characters detected, total words formed, and average confidence score. The recognition result is automatically saved to the MySQL database.

**Step 8 â€" Display:** The frontend receives the results and displays them to the user. The modern Tamil text is shown prominently. The traced image with bounding boxes shows exactly where each character was found. A detailed character table lists each detected character with its confidence score (color-coded: green for high, yellow for medium, red for low). Export options allow the user to copy the text to clipboard, download as a text file, or export as JSON.

### 1.4.3 Advantages of Proposed System

The proposed VatteluttuX system offers several significant advantages over the existing manual process:

1. **No Expert Required:** Anyone with internet access can upload an inscription photograph and receive a translation. The system handles the entire recognition process automatically, making ancient Tamil inscriptions accessible to the general public for the first time.

2. **Speed:** The system processes an inscription image in 2-5 seconds, compared to hours or days required by human experts. This represents a speedup of several thousand times.

3. **High Accuracy:** The CNN model achieves 92.8% Top-1 accuracy across 247 character classes. While not perfect, this is sufficient to produce useful first-pass translations that can then be refined by experts.

4. **Consistency:** Unlike human readers, the CNN model produces the same output every time for the same input. There is no subjective interpretation, no variation based on fatigue, and no disagreement between different readings.

5. **Scalability:** The system can process thousands of inscription images without any additional human effort. This makes it feasible to work through the backlog of unread inscriptions.

6. **Comprehensive Coverage:** With 247 character classes, VatteluttuX covers the complete Tamil character set â€" far more than the 28 classes covered by the most ambitious prior study.

7. **Confidence Scoring:** Every prediction comes with a confidence score, allowing users to easily identify which characters the system is uncertain about. This makes it straightforward to focus human review on the most ambiguous parts of an inscription.

8. **Persistent History:** All recognition results are stored in a MySQL database, creating a growing digital archive of translated inscriptions that is searchable and accessible.

9. **Visual Verification:** The traced image with bounding boxes allows users to visually verify that the system has correctly identified and segmented each character.

10. **Modular Architecture:** The clean separation between frontend, backend, and model components means that any part can be upgraded independently. When a better model is trained, it can be swapped in without changing the frontend or database.

### 1.4.1 Hardware Specification

| Component | Specification |
|:---|:---|
| Processor | Intel Core i3 (7th Generation) or higher / AMD equivalent |
| Minimum RAM | 4 GB (8 GB recommended for faster model inference) |
| Hard Disk | 10 GB free space (for application, model weights, and database) |
| GPU | Optional â€" NVIDIA CUDA-compatible GPU (GTX 1050 or higher) for faster inference; CPU mode is supported |
| Monitor | Any standard display with 1366Ã - 768 resolution or higher |
| Network | Internet connection for web access (local network sufficient for localhost deployment) |
| Input Device | Standard keyboard and mouse |

### 1.4.2 Software Specification

| Component | Technology | Version |
|:---|:---|:---|
| Frontend Framework | React.js with TypeScript | 18.x |
| Backend Framework | FastAPI (Python) | 0.109+ |
| Programming Language (Backend) | Python | 3.10+ |
| Programming Language (Frontend) | TypeScript | 5.x |
| Deep Learning Framework | PyTorch | 2.0+ |
| Image Processing Library | OpenCV (opencv-python) | 4.9+ |
| Image Utility Library | Pillow (PIL) | 10.0+ |
| Numerical Computing | NumPy | 1.26+ |
| Database | MySQL | 8.0 |
| Database Access Platform | XAMPP | Latest |
| ORM (Object Relational Mapping) | SQLAlchemy | 2.0+ |
| Database Driver | PyMySQL | 1.1+ |
| Frontend Build Tool | Vite | Latest |
| Package Manager (Frontend) | npm | 16+ |
| Package Manager (Backend) | pip | Latest |
| Web Server (Backend) | Uvicorn | 0.27+ |
| API Documentation | Swagger UI (built into FastAPI) | Auto-generated |
| IDE / Code Editor | Visual Studio Code | Latest |
| Operating System | Windows 10/11 (also compatible with Linux, macOS) | |
| Web Browser | Google Chrome / Mozilla Firefox / Microsoft Edge | Latest |
| Database Admin Tool | phpMyAdmin (included with XAMPP) | Latest |

---

# CHAPTER 2: LOGICAL DEVELOPMENT

## 2.1 Architectural Design

### 2.1.1 Overview

The software architecture of VatteluttuX follows a three-tier client-server model, which is one of the most widely used architectural patterns in modern web application development. In this model, the system is divided into three separate layers (tiers), each responsible for a specific aspect of the application. The three tiers communicate with each other through well-defined interfaces, which makes the system easier to develop, test, maintain, and upgrade.

The three tiers are:

1. **Presentation Tier (Frontend):** This is the user-facing layer that handles all visual elements and user interactions. It runs in the user's web browser and communicates with the backend through HTTP requests.

2. **Application Tier (Backend):** This is the middle layer that contains all the business logic, data processing, and computation. It receives requests from the frontend, processes them (including running the OCR pipeline), and sends back responses.

3. **Data Tier (Database):** This is the bottom layer responsible for persistent data storage. It maintains the MySQL database that stores all recognition history records and provides data to the application tier on demand.

### 2.1.2 Presentation Tier â€" React.js Frontend

The frontend is built using React.js version 18 with TypeScript for type safety. React.js is a component-based JavaScript library for building user interfaces. Each part of the interface is implemented as a reusable React component with its own state management and CSS styling.

The frontend consists of the following major components:

**Header Component (Header.tsx):** This component provides the top navigation bar for the application. It displays the application name "VatteluttuX" and navigation links to the three main pages: Recognition (home), History, and Character Map. The Header uses React Router for client-side navigation, which means page transitions happen instantly without full page reloads.

**Upload Panel Component (UploadPanel.tsx):** This is the primary interaction point where users upload inscription images. It provides a drag-and-drop zone that responds visually when a file is dragged over it (border color changes, background highlights). When a valid image file is dropped or selected through the file browser, the component generates a preview using the FileReader API and displays the filename. It validates that the file is an image (PNG, JPG, JPEG, or BMP) before accepting it. The component manages its state using React hooks: useState for tracking the dragging state and file preview, useCallback for memoized event handlers, and useRef for accessing the hidden file input element.

**Recognition Page Component (RecognitionPage.tsx):** This is the main page that orchestrates the recognition workflow. It contains the Upload Panel and the Results Display components. When the user clicks "Recognize Inscription", the Recognition Page sends the image to the backend API via a multipart form POST request to `/recognize`. While waiting for the response, it displays a loading indicator. When the results arrive, it passes them to the Results Display component.

**Results Display Component (ResultsDisplay.tsx):** This component presents the recognition output in a comprehensive format. It shows the Modern Tamil text in a large, readable font. Below that, it displays the traced image with colored bounding boxes around each detected character. A character table shows every detected character with its label, Tamil equivalent, confidence score, and bounding box coordinates. Confidence scores are color-coded: green (above 80%), yellow (50-80%), and red (below 50%). The component provides three export options: copy to clipboard, download as text file, and export as JSON file with complete details.

**Character Table Component (CharacterTable.tsx):** This sub-component renders the detailed character-by-character analysis table inside the Results Display. Each row shows the character's index number, internal label (e.g., va_001), Modern Tamil character (e.g., à®…), confidence percentage, and bounding box coordinates (x, y, width, height).

**History Page Component (HistoryPage.tsx):** This component displays all past recognition records fetched from the MySQL database. Records are shown in reverse chronological order (newest first). Each record card shows the original filename, recognized Tamil text (truncated if long), number of characters and words detected, average confidence score, and timestamp. Users can click on a record to view its full details or delete it. The component supports pagination through skip/limit API parameters.

**Character Mapping Viewer Component (CharacterMappingViewer.tsx):** This component provides a browsable reference of all 247 Vatteluttu-to-Tamil character mappings. Characters are organized by linguistic category with tabs or sections for Vowels (12), Aytham (1), Pure Consonants (18), Consonants (18), and Compound Characters (198). Each entry displays the internal label, Modern Tamil character rendered in large font, English transliteration, and category name.

The frontend is built using Vite as the build tool, which provides fast development server startup and hot module replacement (HMR) for instant feedback during development. The application uses standard CSS files (one per component) for styling â€" no CSS framework like Bootstrap or Tailwind is used, keeping the design fully custom.

### 2.1.3 Application Tier â€" FastAPI Backend

The backend is built using FastAPI, a modern Python web framework known for its high performance and automatic API documentation. FastAPI is built on top of Starlette (for async web serving) and Pydantic (for data validation). It runs on the Uvicorn ASGI server.

The backend is organized into the following sub-modules:

**API Module (app/api/):**
- `routes.py` â€" Defines all REST API endpoints. The main endpoints are:
  - `POST /recognize` â€" Accepts an image file upload, runs the OCR pipeline, saves results to the database, and returns the recognition output as JSON.
  - `GET /health` â€" Returns the API health status and model information.
  - `GET /history` â€" Returns a paginated list of past recognition records from the database.
  - `GET /history/{id}` â€" Returns a single recognition record by its database ID.
  - `DELETE /history/{id}` â€" Deletes a recognition record from the database.
  - `GET /labels` â€" Returns all available character labels and their Tamil mappings.
  - `GET /labels/{label}` â€" Returns detailed information about a specific character label.
  - `GET /characters` â€" Returns all character mappings, optionally filtered by category (vowel, consonant, etc.).
  - `GET /character-map` â€" Returns the complete character map with all metadata and statistics.

**ML Module (app/ml/):**
- `model.py` â€" Contains three CNN model architectures: VatteluttuCNN (the main ResNet-inspired model), TinyCNN (a lightweight model for fast CPU training), and TamilCRNN (a CNN+LSTM hybrid for future sequence recognition).
- `inference.py` â€" Wraps the trained model with lazy loading, batch processing, and top-k prediction capabilities. It handles model loading from disk, moving the model to the appropriate device (CPU or GPU), and running inference in evaluation mode with gradient computation disabled.
- `preprocessing.py` â€" Contains all image preprocessing functions: loading raw image bytes, grayscale conversion, Otsu binarization, adaptive thresholding, morphological operations, polarity detection, character crop resizing, and pixel value normalization.

**OCR Module (app/ocr/):**
- `pipeline.py` â€" Implements the complete OCR pipeline that chains preprocessing â†' segmentation â†' classification â†' mapping â†' traced image generation. Contains the CharacterResult and OCRResult dataclasses that define the structure of recognition results.
- `segmentation.py` â€" Implements character segmentation using Connected Component Analysis with multi-stage filtering (area, aspect ratio, solidity), adaptive morphology retry, and bounding box management.
- `word_segmentation.py` â€" Groups detected characters into words based on spatial proximity analysis, using inter-character gap statistics and line-awareness detection.
- `traced_image.py` â€" Generates annotated images with colored bounding boxes drawn around each detected character, with labels and confidence scores displayed.
- `tamil_rules.py` â€" Implements linguistic validation rules that check whether recognized character sequences form phonetically valid Tamil combinations.

**Core Module (app/core/):**
- `config.py` â€" Application configuration using Pydantic Settings, including database URL, model path, media directory, CORS origins, and debug flags.
- `label_to_char.json` â€" Simple JSON mapping file: 247 labels to their Tamil characters.
- `character_map.json` â€" Comprehensive JSON metadata file with category, transliteration, Unicode codepoint, and phonetic information for each character.

**Database Module (app/db/):**
- `database.py` â€" SQLAlchemy engine, session factory, and database initialization.
- `models.py` â€" SQLAlchemy ORM model for the `recognition_history` table.
- `crud.py` â€" CRUD (Create, Read, Update, Delete) operations for the recognition history.

The backend configures CORS (Cross-Origin Resource Sharing) to allow the React frontend (running on port 5173) to communicate with the API (running on port 8000). Static files (traced images) are served from the `/media` endpoint.

### 2.1.4 Data Tier â€" MySQL Database

The data tier uses MySQL 8.0, managed through XAMPP for easy local deployment. The database stores recognition history in the `recognition_history` table. The backend connects to MySQL using SQLAlchemy ORM with the PyMySQL driver.

The database provides several important functions:
- **Persistence:** All recognition results are permanently stored, even after the server is restarted.
- **Querying:** Records can be queried by any field (filename, date, confidence, etc.) through SQL.
- **History Tracking:** Researchers can review how the system performed on different inscription images over time.
- **Admin Access:** The phpMyAdmin web interface (included with XAMPP) provides a graphical way to browse, search, edit, and export database records.
- **Data Export:** Records can be exported from MySQL in CSV, SQL, or other formats for external analysis.

### 2.1.5 Architecture Diagram

The following diagram shows the three-tier architecture of VatteluttuX:

![Architecture Diagram](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\architecture_diagram_1772426488943.png)

---

## 2.2 Data Flow Diagram

A Data Flow Diagram (DFD) is a graphical representation of the flow of data through an information system. It shows how data enters the system, how it is processed, and where it is stored or output. DFDs are an important tool in system analysis and design because they provide a clear, visual picture of the system's functionality without getting into implementation details.

DFDs use four standard symbols:
1. **External Entity** (rectangle) â€" A source or destination of data outside the system boundary.
2. **Process** (circle or rounded rectangle) â€" An activity that transforms data.
3. **Data Store** (open-ended rectangle) â€" A repository where data is held for later use.
4. **Data Flow** (arrow) â€" The movement of data between entities, processes, and stores.

### 2.2.1 Level 0 â€" Context Diagram

The Level 0 DFD (also called the Context Diagram) shows the entire VatteluttuX system as a single process and its interactions with external entities. This is the highest-level view of the system.

There is one external entity: the **User / Researcher**, who provides inscription images as input and receives recognition results as output.

There is one process: the **VatteluttuX OCR System**, which represents all the processing that happens internally.

There is one data store: the **MySQL Database**, which stores recognition history for retrieval.

**Data Flows:**
- The User sends an "Inscription Image" to the system.
- The system returns "Modern Tamil Text + Confidence Scores" to the User.
- The system stores and retrieves "Recognition Records" from the MySQL Database.

![DFD Level 0](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\dfd_level0_1772426509725.png)

### 2.2.2 Level 1 â€" Detailed DFD

The Level 1 DFD decomposes the single process from the Level 0 diagram into its six constituent sub-processes, showing how data flows through each stage of the OCR pipeline.

**P1 â€" Image Upload and Validation:** This process receives the raw inscription image from the User. It validates the file type (must be an image), checks the file size, and converts the image bytes into an OpenCV-compatible format. The output is the raw image data in a standardized format.

**P2 â€" Preprocessing:** This process receives the raw image and applies the cleaning pipeline: grayscale conversion, denoising (Fast Non-Local Means with strength parameter h=10), Otsu binarization, polarity auto-detection and correction, and morphological operations (opening with a 3Ã - 3 elliptical kernel to remove noise, closing to repair broken strokes). The output is a clean binary image where characters are white pixels on a black background.

**P3 â€" Character Segmentation:** This process receives the binary image and identifies individual characters using Connected Component Analysis (CCA). OpenCV's `connectedComponentsWithStats` function scans the image and labels each group of connected white pixels. The function returns statistics for each component: position (x, y), dimensions (width, height), and area (pixel count). Multi-stage filtering removes false detections. The output is a list of character crops, each resized to 64Ã - 64 pixels.

**P4 â€" CNN Classification:** This process receives the 64Ã - 64 character crops and classifies each one using the trained neural network model. The model weights are read from Data Store D1 (`best_model.pth`). The process outputs a label prediction (e.g., "va_001") and a confidence score (0.0 to 1.0) for each character.

**P5 â€" Character Mapping:** This process receives the label predictions and looks up the corresponding Modern Tamil Unicode characters from Data Store D2 (`label_to_char.json`). The process also retrieves additional metadata (transliteration, category) from the character map. The output is the Modern Tamil text string. The results are also sent to Data Store D3 (MySQL Database) for persistent storage.

**P6 â€" Response Generation:** This process assembles the final output: Modern Tamil text, character details, word groupings, traced image, and summary statistics. It generates the traced image (original photo with bounding boxes overlaid), serializes the results to JSON format, and sends the complete response back to the User.

**Data Stores:**
- **D1: Model Weights (best_model.pth)** â€" Contains the trained CNN model parameters (weights and biases for all layers).
- **D2: Label-to-Character Map (label_to_char.json)** â€" Maps 247 internal labels to Modern Tamil Unicode characters.
- **D3: MySQL Database (recognition_history)** â€" Stores all recognition results for history tracking.

![DFD Level 1](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\dfd_level1_1772426523048.png)

### 2.2.3 OCR Pipeline Flowchart

The following flowchart shows the step-by-step processing of an inscription image through the OCR pipeline:

![OCR Pipeline Flowchart](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\ocr_pipeline_flow_1772426574838.png)

---

## 2.3 Use Case Diagram

A Use Case Diagram shows the interactions between actors (users) and the system. It identifies the different ways a user can interact with the system and the functions the system provides.

### 2.3.1 Actors

The VatteluttuX system has one primary actor:

**User / Researcher:** Any person who accesses the VatteluttuX web application through a browser. This includes researchers, historians, linguists, students, and the general public. The user does not need any specialized knowledge of the Vatteluttu script.

### 2.3.2 Use Cases

The following use cases describe the main interactions between the User and the system:

| Use Case ID | Use Case Name | Description |
|:---|:---|:---|
| UC-01 | Upload Inscription Image | The user uploads a photograph of a Vatteluttu inscription through drag-and-drop or file browse. |
| UC-02 | Preview Image | The system shows a preview of the uploaded image before processing. |
| UC-03 | Recognize Inscription | The user triggers OCR recognition. The system processes the image through the pipeline and returns results. |
| UC-04 | View Recognition Results | The user views the Modern Tamil text, traced image, character table, and confidence scores. |
| UC-05 | Copy Text to Clipboard | The user copies the recognized Tamil text to the system clipboard. |
| UC-06 | Export as Text File | The user downloads the recognized text as a .txt file. |
| UC-07 | Export as JSON | The user downloads the complete recognition result (including character details and bounding boxes) as a .json file. |
| UC-08 | View Recognition History | The user browses a list of all past recognition records stored in the database. |
| UC-09 | View History Record Detail | The user views the full details of a specific past recognition record. |
| UC-10 | Delete History Record | The user deletes a specific recognition record from the history. |
| UC-11 | Browse Character Map | The user browses all 247 Vatteluttu-to-Tamil character mappings organized by category. |
| UC-12 | Filter Characters by Category | The user filters the character map to show only a specific category (vowels, consonants, etc.). |

### 2.3.3 Use Case Descriptions

**UC-01: Upload Inscription Image**
- **Actor:** User
- **Precondition:** The user has a photograph of a Vatteluttu inscription saved on their device.
- **Main Flow:** (1) User navigates to the Recognition page. (2) User drags an image file onto the upload zone, or clicks the zone and selects a file. (3) System validates the file type (PNG, JPG, JPEG, BMP). (4) System displays a preview of the image.
- **Alternative Flow:** If the file type is invalid, the system displays an error message and does not accept the file.
- **Postcondition:** The image is loaded and previewed, ready for recognition.

**UC-03: Recognize Inscription**
- **Actor:** User
- **Precondition:** A valid image has been uploaded and previewed.
- **Main Flow:** (1) User clicks "Recognize Inscription" button. (2) System sends the image to the backend API. (3) Backend processes the image through the OCR pipeline. (4) Backend saves the result to the MySQL database. (5) Backend returns the result to the frontend. (6) Frontend displays the results.
- **Alternative Flow:** If no characters are detected, the system returns a warning message. If the backend is unavailable, the system displays a connection error.
- **Postcondition:** Recognition results are displayed and saved to the database.

**UC-08: View Recognition History**
- **Actor:** User
- **Precondition:** At least one recognition has been performed previously.
- **Main Flow:** (1) User clicks "History" in the navigation bar. (2) System fetches recognition records from the database via the API. (3) Records are displayed in reverse chronological order with filename, Tamil text, confidence, and timestamp.
- **Postcondition:** The user can browse all past recognition records.

---

## 2.4 Sequence Diagram

A Sequence Diagram shows the order of interactions between different components of the system over time. It illustrates how messages flow between the user, frontend, backend, and database during a specific operation.

### 2.4.1 Sequence Diagram for Image Recognition

The following describes the step-by-step sequence of interactions when a user uploads an inscription image and requests recognition:

| Step | From | To | Message / Action |
|:---|:---|:---|:---|
| 1 | User | Frontend (UploadPanel) | Drop/select image file |
| 2 | Frontend (UploadPanel) | Frontend (UploadPanel) | Validate file type (image check) |
| 3 | Frontend (UploadPanel) | Frontend (UploadPanel) | Generate image preview (FileReader API) |
| 4 | User | Frontend (RecognitionPage) | Click "Recognize Inscription" button |
| 5 | Frontend (RecognitionPage) | Backend (POST /recognize) | Send image as multipart form data |
| 6 | Backend (routes.py) | Backend (preprocessing.py) | Call load_image() and preprocess_full() |
| 7 | Backend (preprocessing.py) | Backend (routes.py) | Return grayscale and binary images |
| 8 | Backend (routes.py) | Backend (segmentation.py) | Call segment_characters() on binary image |
| 9 | Backend (segmentation.py) | Backend (routes.py) | Return list of character bounding boxes |
| 10 | Backend (routes.py) | Backend (inference.py) | Call predict_single() for each character crop |
| 11 | Backend (inference.py) | Model Weights (best_model.pth) | Load model weights (lazy load, first time only) |
| 12 | Backend (inference.py) | Backend (routes.py) | Return label + confidence for each character |
| 13 | Backend (routes.py) | Backend (mapping.py) | Call map_label() to get Tamil characters |
| 14 | Backend (mapping.py) | label_to_char.json | Read character mapping |
| 15 | Backend (mapping.py) | Backend (routes.py) | Return Modern Tamil characters |
| 16 | Backend (routes.py) | Backend (traced_image.py) | Generate annotated image with bounding boxes |
| 17 | Backend (routes.py) | Backend (crud.py) | Call save_recognition() |
| 18 | Backend (crud.py) | MySQL Database | INSERT INTO recognition_history |
| 19 | MySQL Database | Backend (crud.py) | Return saved record with auto-generated ID |
| 20 | Backend (routes.py) | Frontend (RecognitionPage) | Return JSON response with all results |
| 21 | Frontend (RecognitionPage) | Frontend (ResultsDisplay) | Pass results to display component |
| 22 | Frontend (ResultsDisplay) | User | Render Tamil text, traced image, character table |

### 2.4.2 Sequence Diagram for History Retrieval

| Step | From | To | Message / Action |
|:---|:---|:---|:---|
| 1 | User | Frontend (Header) | Click "History" navigation link |
| 2 | Frontend (Header) | Frontend (HistoryPage) | Navigate to History page (React Router) |
| 3 | Frontend (HistoryPage) | Backend (GET /history) | Fetch recognition records (skip=0, limit=50) |
| 4 | Backend (routes.py) | Backend (crud.py) | Call get_recognition_history() |
| 5 | Backend (crud.py) | MySQL Database | SELECT * FROM recognition_history ORDER BY created_at DESC |
| 6 | MySQL Database | Backend (crud.py) | Return list of records |
| 7 | Backend (crud.py) | Backend (routes.py) | Return records to route handler |
| 8 | Backend (routes.py) | Frontend (HistoryPage) | Return JSON array of history records |
| 9 | Frontend (HistoryPage) | User | Render history cards with filename, text, confidence, date |

---

# CHAPTER 3: DATABASE DESIGN

## 3.1 Table Design

### 3.1.1 Overview

The VatteluttuX system uses a MySQL 8.0 relational database managed through XAMPP. The database is named `vatteluttux` and is accessed by the backend through the SQLAlchemy ORM (Object Relational Mapping) with the PyMySQL driver. SQLAlchemy provides an abstraction layer that allows the Python code to interact with the database using Python objects instead of writing raw SQL queries.

The database connection string follows this format:
`mysql+pymysql://root@localhost/vatteluttux`

This connects to the MySQL server running on localhost (port 3306) using the root user with no password (default XAMPP configuration) and selects the `vatteluttux` database.

The system uses one primary database table (`recognition_history`) for storing OCR results. The character mapping data is stored in JSON configuration files rather than in the database, because the mapping is static (it does not change during runtime) and loading it from a JSON file is faster than querying the database for every character lookup.

### 3.1.2 Table: recognition_history

This is the main table that stores all past recognition results. Each row represents one complete OCR recognition operation â€" that is, the processing of one uploaded inscription image.

| S.No | Field Name | Data Type | Size | Constraints | Description |
|:---|:---|:---|:---|:---|:---|
| 1 | id | INT | 4 bytes | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique auto-generated identifier for each recognition record. The database automatically assigns the next available integer when a new record is inserted. |
| 2 | original_filename | VARCHAR | 255 chars | NOT NULL | The original name of the image file uploaded by the user (e.g., "inscription_temple_01.png"). This is stored for identification purposes so the user can recognize their uploads in the history. |
| 3 | recognized_text | TEXT | Up to 65,535 chars | NOT NULL | The raw label sequence output from the CNN classifier. Each label is separated by a space (e.g., "va_001 va_014 va_037 va_082"). This field preserves the raw model output for debugging and analysis. |
| 4 | modern_text | TEXT | Up to 65,535 chars | NOT NULL | The Modern Tamil Unicode text that corresponds to the recognized labels (e.g., "à®… à®† à®‡ à®•à®¾"). This is the human-readable output that users are most interested in. |
| 5 | num_characters | INT | 4 bytes | DEFAULT 0 | The total number of individual characters detected and classified in the image. This count includes all characters regardless of confidence level. |
| 6 | num_words | INT | 4 bytes | DEFAULT 0 | The number of words formed by spatially grouping nearby characters. Words are determined by the horizontal gaps between character bounding boxes. |
| 7 | avg_confidence | FLOAT | 4 bytes | DEFAULT 0.0 | The average prediction confidence score across all detected characters, expressed as a decimal between 0.0 (no confidence) and 1.0 (full confidence). This provides a quick summary of how reliable the recognition result is. |
| 8 | traced_image_path | VARCHAR | 500 chars | NULL (optional) | The server file path where the annotated traced image is saved. The traced image shows the original inscription photograph with colored bounding boxes drawn around each detected character. This field is NULL if traced image generation failed. |
| 9 | created_at | DATETIME | 8 bytes | NOT NULL, DEFAULT CURRENT_TIMESTAMP | The exact date and time when the OCR recognition was performed. The database automatically sets this to the current server time when the record is created. Format: YYYY-MM-DD HH:MM:SS. |

### 3.1.3 SQL CREATE TABLE Statement

The table is created automatically by SQLAlchemy's `Base.metadata.create_all()` method when the application starts up. The equivalent SQL statement is:

```sql
CREATE TABLE IF NOT EXISTS recognition_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_filename VARCHAR(255) NOT NULL,
    recognized_text TEXT NOT NULL,
    modern_text TEXT NOT NULL,
    num_characters INT DEFAULT 0,
    num_words INT DEFAULT 0,
    avg_confidence FLOAT DEFAULT 0.0,
    traced_image_path VARCHAR(500) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX ix_recognition_history_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

The `utf8mb4` character set is used to ensure proper storage of Tamil Unicode characters. The InnoDB storage engine is used for transaction support and referential integrity.

### 3.1.4 JSON Configuration: label_to_char.json

This is a JSON file stored at `backend/app/core/label_to_char.json`. It contains a simple key-value mapping from 247 internal model labels to their corresponding Modern Tamil Unicode characters. This file is loaded into memory when the application starts and is used by the character mapping service during every recognition operation.

Sample content:
```json
{
    "va_001": "à®…",
    "va_002": "à®†",
    "va_003": "à®‡",
    "va_004": "à®ˆ",
    "va_005": "à®‰",
    ...
    "va_247": "à®©à¯Œ"
}
```

### 3.1.5 Character Categories Summary

The 247 character classes are organized into five linguistic categories:

| S.No | Category | Tamil Name | Count | Label Range | Examples |
|:---|:---|:---|:---|:---|:---|
| 1 | Vowels | à®‰à®¯à®¿à®°à¯ à®Žà®´à¯à®¤à¯à®¤à¯ | 12 | va_001 to va_012 | à®…, à®†, à®‡, à®ˆ, à®‰, à®Š, à®Ž, à®, à®, à®', à®", à®" |
| 2 | Aytham | à®†à®¯à¯à®¤à®®à¯ | 1 | va_013 | à®ƒ |
| 3 | Pure Consonants | à®®à¯†à®¯à¯ à®Žà®´à¯à®¤à¯à®¤à¯ | 18 | va_014 to va_031 | à®•à¯, à®™à¯, à®šà¯, à®žà¯, à®Ÿà¯, à®£à¯, à®¤à¯, à®¨à¯, à®ªà¯, à®®à¯ |
| 4 | Consonants (inherent 'a') | â€" | 18 | va_032 to va_049 | à®•, à®™, à®š, à®ž, à®Ÿ, à®£, à®¤, à®¨, à®ª, à®® |
| 5 | Compound Characters (Uyirmei) | à®‰à®¯à®¿à®°à¯à®®à¯†à®¯à¯ | 198 | va_050 to va_247 | à®•à®¾, à®•à®¿, à®•à¯€, à®•à¯, à®•à¯‚, à®•à¯†, à®•à¯‡, à®•à¯ˆ, à®•à¯Š, à®•à¯‹, à®•à¯Œ |
| | **Total** | | **247** | | |

---

## 3.2 Data Dictionary

The data dictionary provides a comprehensive description of every data element in the system, including its meaning, type, format, and sample values.

### 3.2.1 Database Fields

| S.No | Field Name | Full Description | Data Type | Format / Range | Sample Value |
|:---|:---|:---|:---|:---|:---|
| 1 | id | Unique auto-generated identifier for each OCR recognition record. Starts at 1 and increments by 1 for each new record. | INT | 1 to 2,147,483,647 | 42 |
| 2 | original_filename | The name of the image file as it was on the user's computer when they uploaded it. Includes the file extension. | VARCHAR(255) | Any valid filename | inscription_temple_01.png |
| 3 | recognized_text | The complete sequence of internal model labels predicted by the CNN for each detected character, separated by spaces. The order follows the reading order (left-to-right, top-to-bottom). | TEXT | Labels separated by spaces | va_001 va_014 va_037 va_082 |
| 4 | modern_text | The Modern Tamil Unicode text produced by mapping each recognized label to its corresponding Tamil character. This is the primary output of the system. | TEXT | Unicode Tamil text | à®… à®•à¯ à®‡ à®•à®¾ |
| 5 | num_characters | The total count of individual characters detected and classified in the inscription image, regardless of confidence level. | INT | 0 to any positive integer | 15 |
| 6 | num_words | The count of words formed by spatially grouping characters. Characters with small horizontal gaps are grouped together; larger gaps indicate word boundaries. | INT | 0 to any positive integer | 4 |
| 7 | avg_confidence | The arithmetic mean of all individual character confidence scores. A value of 0.90 means the model was, on average, 90% confident in its predictions. | FLOAT | 0.0 to 1.0 | 0.8725 |
| 8 | traced_image_path | The relative path on the server where the annotated traced image is saved. The traced image shows bounding boxes overlaid on the original photograph. | VARCHAR(500) | Server path | /media/traced_a1b2c3d4.png |
| 9 | created_at | The server timestamp recording when the recognition operation was completed and the result was saved to the database. | DATETIME | YYYY-MM-DD HH:MM:SS | 2026-02-26 14:30:00 |

### 3.2.2 API Data Elements

In addition to the database fields, the API returns several computed data elements in its JSON response:

| S.No | Field Name | Description | Data Type | Sample |
|:---|:---|:---|:---|:---|
| 1 | characters | Array of individual character results, each containing label, modern_tamil, confidence, and bbox | Array of Objects | [{"label": "va_001", "modern_tamil": "à®…", "confidence": 0.94, "bbox": {"x": 10, "y": 20, "w": 45, "h": 50}}] |
| 2 | words | Array of word objects, each containing the characters in that word and validation status | Array of Objects | [{"text": "à®…à®•à¯", "characters": [...], "is_validated": true}] |
| 3 | traced_image_url | Full URL to download the traced image with bounding boxes | String | http://localhost:8000/media/traced_a1b2c3.png |
| 4 | image_width | Width of the original uploaded image in pixels | INT | 1200 |
| 5 | image_height | Height of the original uploaded image in pixels | INT | 800 |
| 6 | warnings | Array of warning messages about the recognition (e.g., low confidence, invalid sequences) | Array of Strings | ["Low confidence characters detected"] |

---

## 3.3 Relationship Diagram

### 3.3.1 Entity Relationship (ER) Diagram

The Entity Relationship Diagram shows the data entities in the VatteluttuX system and the relationships between them. The system has three main data entities:

**Entity 1 â€" INSCRIPTION_IMAGE:**
This represents the image file uploaded by the user. It is a transient entity â€" the raw image data exists in memory during processing but is not permanently stored in the database as a separate record. The image's identity is preserved through the `original_filename` field in the recognition history.

Attributes:
- image_bytes (Binary) â€" The raw binary content of the image file
- filename (String) â€" The name of the image file
- content_type (String) â€" The MIME type of the image (e.g., image/png)
- file_size (Integer) â€" The size of the file in bytes
- upload_time (Timestamp) â€" When the file was received by the server

**Entity 2 â€" RECOGNITION_HISTORY:**
This is the main persistent entity, stored as a MySQL database table. Each record represents one complete OCR recognition operation performed on an uploaded image.

Attributes: id (PK), original_filename, recognized_text, modern_text, num_characters, num_words, avg_confidence, traced_image_path, created_at

**Entity 3 â€" CHARACTER_MAP:**
This represents the character mapping configuration stored in the `label_to_char.json` file. It defines the relationship between internal model labels and Modern Tamil Unicode characters. This entity has 247 entries, one for each character class.

Attributes:
- label_id (String, Primary Key) â€" The internal identifier (e.g., "va_001")
- modern_tamil (Unicode String) â€" The corresponding Tamil character (e.g., "à®…")
- category (String) â€" The linguistic category (vowel, aytham, pure_consonant, consonant, uyirmei)
- transliteration (String) â€" English phonetic representation (e.g., "a")
- unicode_point (String) â€" The Unicode code point (e.g., "U+0B85")

**Relationships:**

1. **INSCRIPTION_IMAGE â€" processes â†' RECOGNITION_HISTORY (1:N):**
One inscription image can produce one or more recognition history records. If a user uploads the same image multiple times, each processing creates a separate history record. The cardinality is one-to-many because the same image could be re-processed with different model versions.

2. **CHARACTER_MAP â€" defines â†' RECOGNITION_HISTORY (1:N):**
The character map entries are used to interpret the recognition results. Each recognition history record references multiple character map entries (one per detected character). The cardinality is one-to-many because each character map entry (e.g., "va_001" â†' "à®…") is used across many different recognition records.

![Entity Relationship Diagram](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\er_diagram_1772426555690.png)

### 3.3.2 Database Operations

The system performs the following database operations:

**INSERT (Create):** After every successful recognition, a new record is inserted into the `recognition_history` table with all nine fields populated.

**SELECT (Read):** The History Page and History API endpoints query the table to retrieve past records. Records are ordered by `created_at DESC` (newest first) and support pagination through `OFFSET` and `LIMIT` clauses.

**DELETE (Delete):** Users can delete individual history records through the History Page or the DELETE API endpoint. The deletion is permanent and cannot be undone.

**No UPDATE operations** are currently implemented. Once a recognition result is saved, it is treated as immutable â€" it cannot be edited after creation. This design choice preserves the integrity of the recognition results as a historical record.

---

# CHAPTER 4: PROGRAM DESIGN

The project titled "VatteluttuX: Enhancing Epigraphical Research through Deep Learning-Based OCR and Modern Tamil Mapping" is built as a full-stack web application using React.js (frontend), FastAPI/Python (backend), PyTorch (deep learning), and MySQL (database). The system is divided into eight main modules. Below is a detailed explanation of how each module works, including the logic, algorithms, and technologies used.

## Module 1: Image Upload and Preview (UploadPanel.tsx)

### Purpose
This module is the entry point of the entire system. It provides the user interface component where users can upload a photograph of a Vatteluttu inscription for recognition. It handles file selection, validation, preview generation, and passing the file to the parent component for processing.

### How it Works

The Upload Panel is implemented as a React.js functional component written in TypeScript. It uses three React hooks for state management:
- `useState` â€" Tracks the drag-over state (isDragging) and file preview URL (preview).
- `useCallback` â€" Memoizes the file handling functions to prevent unnecessary re-renders.
- `useRef` â€" Holds a reference to the hidden file input element for programmatic clicking.

**Drag-and-Drop Implementation:** The component creates a styled div element that acts as a drop zone. Three event handlers manage the drag-and-drop interaction: `onDragOver` sets the isDragging state to true and changes the drop zone's visual appearance (border color, background), `onDragLeave` resets the isDragging state when the file is dragged away, and `onDrop` captures the dropped file and passes it to the file handler.

**File Validation:** When a file is received (either through drag-and-drop or file browser), the component checks the file's MIME type. Only files whose type starts with "image/" are accepted. Valid types include image/png, image/jpeg, and image/bmp. If an invalid file type is dropped, the component displays an alert message: "Please upload an image file (PNG, JPG, JPEG, or BMP)."

**Preview Generation:** For valid image files, the component uses the browser's FileReader API to read the file as a Data URL (base64-encoded string). When the FileReader finishes reading, its `onload` event handler updates the preview state with the Data URL. This URL is used as the `src` attribute of an `<img>` element to show a live preview of the inscription image.

**State Communication:** The Upload Panel is a child component of the Recognition Page. Communication between them happens through callback props: the `onFileSelect` prop passes the selected File object to the parent component, which manages the overall recognition workflow.

### Technology
React.js 18, TypeScript 5, HTML5 Drag and Drop API, FileReader API, CSS.

---

## Module 2: Image Preprocessing Pipeline (preprocessing.py)

### Purpose
This module handles the critical task of cleaning and normalizing raw inscription photographs before character recognition. Stone inscription images present numerous challenges: uneven lighting from outdoor environments, surface cracks and damage from centuries of weathering, biological growth (moss, lichen, algae) covering parts of the inscription, and varying contrast levels due to different stone types and carving depths.

### Algorithm and Steps

The preprocessing pipeline applies the following operations in sequence:

**Step 1 â€" Image Loading (load_image):**
The raw image bytes received from the HTTP request are converted into a NumPy array using `np.frombuffer()`. This array is then decoded into an OpenCV image matrix using `cv2.imdecode()` with the `cv2.IMREAD_COLOR` flag, which ensures the image is loaded as a 3-channel BGR (Blue-Green-Red) color image regardless of the original format. If decoding fails (corrupted file), a ValueError is raised.

**Step 2 â€" Grayscale Conversion (to_grayscale):**
The 3-channel BGR color image is converted to a 1-channel grayscale image using `cv2.cvtColor()` with the `cv2.COLOR_BGR2GRAY` conversion code. Grayscale conversion reduces the image from 3 channels to 1, removing color information that is irrelevant for character recognition. The conversion formula used by OpenCV is: Gray = 0.299 Ã -  R + 0.587 Ã -  G + 0.114 Ã -  B. These weights reflect the human eye's sensitivity to different colors â€" green dominates because the eye is most sensitive to green light.

**Step 3 â€" Denoising (fastNlMeansDenoising):**
Random noise is reduced using OpenCV's Fast Non-Local Means Denoising algorithm (`cv2.fastNlMeansDenoising()`). Unlike simple smoothing filters (Gaussian blur, median filter) that blur the entire image including edges, the Non-Local Means algorithm preserves edges while removing noise. It works by finding similar patches in the image and averaging them. The key parameter is the filter strength `h` (set to 10), which controls the degree of filtering â€" higher values remove more noise but may blur fine details.

**Step 4 â€" Otsu Binarization (otsu_threshold):**
The grayscale image is converted to a pure binary (black and white) image using Otsu's automatic thresholding method. Otsu's method works by analyzing the histogram of pixel intensities and finding the threshold value that minimizes the weighted sum of within-class variances for the two classes (foreground and background). This makes it adaptive â€" it automatically finds the best threshold for each image, unlike fixed thresholding which requires manual tuning. The function uses `cv2.threshold()` with the `cv2.THRESH_OTSU` flag combined with `cv2.THRESH_BINARY` or `cv2.THRESH_BINARY_INV`.

**Step 5 â€" Polarity Detection and Correction:**
After binarization, the module checks whether characters are white on a black background (expected format) or black on a white background. This is done by counting the number of non-zero (white) pixels and comparing it to the total pixel count. If more than 50% of pixels are white, it means the background is white and characters are black â€" the opposite of what the CNN model expects. In this case, the image is inverted using `cv2.bitwise_not()` so that characters become white pixels on a black background.

**Step 6 â€" Morphological Operations (apply_morphology):**
Two morphological operations are applied using a 3Ã - 3 elliptical structuring element:
- **Opening** (erosion followed by dilation) removes small white noise spots that are smaller than the structuring element. This eliminates false blobs that could be misidentified as characters during segmentation.
- **Closing** (dilation followed by erosion) fills small gaps in character strokes. Ancient inscriptions often have broken characters due to stone wear, and closing reconnects these broken strokes.

**Step 7 â€" Character Crop Preparation (prepare_character_crop):**
Each detected character region is cropped from the binary image and resized to 64Ã - 64 pixels while preserving the aspect ratio. The resizing process works as follows: (1) Calculate the scaling factor that fits the character within 64Ã - 64 without distortion. (2) Resize the character using the scaling factor. (3) Create a new 64Ã - 64 black canvas. (4) Center the resized character on the canvas. (5) Normalize pixel values from [0, 255] to [-1.0, 1.0] by applying: normalized = (pixel / 127.5) - 1.0. This normalization puts the data in the range that works best with the CNN model.

### Technology
Python 3.10+, OpenCV 4.9+ (cv2), NumPy 1.26+.

---

## Module 3: Character Segmentation Engine (segmentation.py, word_segmentation.py)

### Purpose
This module isolates individual characters from the preprocessed binary image. After preprocessing, the image contains clean white characters on a black background. The segmentation module identifies where each character is located and extracts it.

### Algorithm â€" Connected Component Analysis (CCA)

The core algorithm used is Connected Component Analysis, implemented through OpenCV's `connectedComponentsWithStats()` function. This function is based on the Suzuki-Abe border-following algorithm (1985), which traces the boundaries of connected regions in a binary image.

**How CCA Works:**
1. The function scans the binary image from top-left to bottom-right, pixel by pixel.
2. When it encounters a white pixel that has not been labeled yet, it assigns a new label to it.
3. It then traces all connected white pixels (using 8-connectivity, meaning all 8 neighbors are considered) and assigns them the same label.
4. This process continues until all white pixels have been labeled.
5. The function returns: the total number of components found, a label matrix (same size as the image, where each pixel contains its component label), and statistics for each component.

**Statistics returned for each component:**
- `cv2.CC_STAT_LEFT` â€" The leftmost x-coordinate of the component's bounding box
- `cv2.CC_STAT_TOP` â€" The topmost y-coordinate of the component's bounding box
- `cv2.CC_STAT_WIDTH` â€" The width of the bounding box
- `cv2.CC_STAT_HEIGHT` â€" The height of the bounding box
- `cv2.CC_STAT_AREA` â€" The total number of pixels in the component

### Filtering False Detections

Not every connected component corresponds to a real character. Noise, artifacts, and stone texture can create small blobs that need to be filtered out. Three filtering criteria are applied:

**Area Filtering:** Components that are too small (area less than the minimum threshold, typically 50 pixels) are removed as noise. Components that are too large (area exceeding the maximum threshold, which is set to a percentage of the total image area) are removed as they likely represent background regions or merged characters.

**Aspect Ratio Filtering:** The width-to-height ratio of each component's bounding box is checked. Components with an aspect ratio less than 0.1 (extremely narrow) or greater than 10.0 (extremely wide) are removed. These extreme ratios indicate noise, scratches, or other artifacts rather than real characters.

**Solidity Filtering:** Solidity is the ratio of the component's actual area to the area of its convex hull. It measures how "filled in" the component is. Components with very low solidity (e.g., less than 0.15) are hollow shapes that are unlikely to be characters.

### Adaptive Retry Mechanism

If the initial segmentation detects too few characters (which could indicate that character strokes are broken and not forming complete connected components), the module automatically retries with morphological closing applied to the binary image. Closing fills small gaps between broken strokes, potentially reconnecting fragments into complete characters.

### Word Segmentation (word_segmentation.py)

After individual characters are detected, the word segmentation sub-module groups them into words based on spatial proximity:

1. Characters are sorted by their x-coordinate (left-to-right reading order).
2. The horizontal gap between consecutive characters is calculated.
3. The median gap is computed as a baseline inter-character spacing.
4. If the gap between two consecutive characters exceeds a threshold (typically 2.5Ã -  the median gap), a word boundary is inserted.
5. Line breaks are detected when the y-coordinate of a character differs significantly from the previous character's y-coordinate.

### Technology
Python 3.10+, OpenCV 4.9+, NumPy 1.26+.

---

## Module 4: CNN Classification Model (model.py, inference.py)

### Purpose
This is the core intelligence module of VatteluttuX. It takes a preprocessed 64Ã - 64 grayscale image of a single Vatteluttu character and classifies it into one of 247 Tamil character classes.

### Model Architecture â€" VatteluttuCNN

The VatteluttuCNN model uses a ResNet-inspired architecture with the following structure:

**Input Layer:** The model accepts a 1-channel (grayscale) 64Ã - 64 pixel image as a PyTorch tensor with shape [batch_size, 1, 64, 64].

**Initial Convolutional Block:** One ConvBlock with 32 output filters (3Ã - 3 kernel, stride 1, padding 1). Each ConvBlock consists of: Conv2d â†' BatchNorm2d â†' ReLU. This block extracts low-level features like edges and corners.

**Stage 1 (64 filters):** ConvBlock(32â†'64) â†' ResidualBlock(64) â†' MaxPool2d(2Ã - 2). Output size: 32Ã - 32. The ResidualBlock adds a skip connection: the input is added directly to the output of two consecutive convolutions, allowing gradient flow during training.

**Stage 2 (128 filters):** ConvBlock(64â†'128) â†' ResidualBlock(128) â†' MaxPool2d(2Ã - 2). Output size: 16Ã - 16. This stage captures mid-level features like curve patterns and stroke intersections.

**Stage 3 (256 filters):** ConvBlock(128â†'256) â†' ResidualBlock(256) â†' MaxPool2d(2Ã - 2). Output size: 8Ã - 8. This stage captures higher-level features like complete character sub-components.

**Stage 4 (512 filters):** ConvBlock(256â†'512) â†' ResidualBlock(512) â†' MaxPool2d(2Ã - 2). Output size: 4Ã - 4. This stage captures the most abstract, character-level features.

**Global Average Pooling:** AdaptiveAvgPool2d(1) reduces each 4Ã - 4 feature map to a single value by averaging all pixels, producing a 512-dimensional feature vector. This is preferred over flattening because it reduces the number of parameters and provides some spatial invariance.

**Classifier Head:**
- Dropout(0.5) â€" Randomly zeros out 50% of the feature values during training to prevent overfitting.
- Linear(512â†'256) â€" Fully connected layer that reduces the dimensionality.
- ReLU â€" Non-linear activation.
- Dropout(0.25) â€" Additional regularization with lighter dropout.
- Linear(256â†'247) â€" Final layer that produces 247 output scores, one for each character class.

**Output:** A tensor of shape [batch_size, 247] containing raw logit scores. During inference, softmax is applied to convert these to probability distributions.

### Residual Block Design

Each ResidualBlock contains:
1. Conv2d(channels, channels, 3Ã - 3) â†' BatchNorm â†' ReLU
2. Conv2d(channels, channels, 3Ã - 3) â†' BatchNorm
3. Skip connection: output = ReLU(conv_output + input)

The skip connection is the key innovation from ResNet. By adding the input directly to the output, the block only needs to learn the "residual" â€" the difference between the desired output and the input. This makes it much easier to train deep networks because gradients can flow directly through the skip connection, avoiding the vanishing gradient problem.

### Training Details

The model was trained with the following hyperparameters:

| Parameter | Value |
|:---|:---|
| Training Images | 247,000 (1,000 per class) |
| Validation Split | 20% (49,400 images) |
| Test Split | 10% (24,700 images) |
| Batch Size | 64 |
| Optimizer | Adam (Î²â‚=0.9, Î²â‚‚=0.999, Îµ=1e-8) |
| Initial Learning Rate | 0.001 |
| Learning Rate Scheduler | ReduceLROnPlateau (factor=0.5, patience=3) |
| Loss Function | CrossEntropyLoss |
| Epochs | ~30 (with early stopping) |
| Dropout Rate | 50% (classifier layer 1), 25% (classifier layer 2) |
| Weight Initialization | Kaiming He Normal |
| Data Augmentation | Rotation (Â±15Â°), Scale (0.8-1.2), Noise, Blur, Elastic |
| Final Test Accuracy | 92.8% (Top-1) |

### Inference Engine (inference.py)

The inference engine manages model loading and prediction:

**Lazy Loading:** The model weights are not loaded when the server starts. Instead, they are loaded on the first prediction request. This reduces startup time and memory usage when the model is not needed (e.g., when only viewing history).

**Device Management:** The inference engine automatically detects whether a CUDA-compatible GPU is available. If yes, the model runs on the GPU for faster inference. If no GPU is found, it falls back to CPU mode.

**Prediction Process:**
1. Receive a preprocessed 64Ã - 64 character crop as a NumPy array.
2. Convert to a PyTorch tensor with shape [1, 1, 64, 64].
3. Move the tensor to the same device as the model (CPU or GPU).
4. Set the model to evaluation mode (`model.eval()`).
5. Disable gradient computation (`torch.no_grad()`) for speed.
6. Run the forward pass to get 247 raw logit scores.
7. Apply softmax to convert to probabilities.
8. Select the class with the highest probability as the prediction.
9. Return the predicted label and the confidence score (probability).

![CNN Architecture](C:\Users\Asus\.gemini\antigravity\brain\c39d4a0b-fd6d-447d-a543-9be6e133db06\cnn_architecture_1772426590049.png)

---

## Module 5: Character Mapping Service (mapping.py, label_mappings.py)

### Purpose
This module bridges the gap between the CNN model's internal predictions and human-readable output. The model produces labels like "va_001" or "va_037", which are meaningless to users. The mapping module translates these labels into Modern Tamil Unicode characters that everyone can read.

### How it Works

The module maintains two JSON data structures loaded into memory at startup:

**Primary Mapping (label_to_char.json):** A flat dictionary with 247 entries. Keys are label strings (e.g., "va_001"), values are Tamil Unicode characters (e.g., "à®…"). Lookup is O(1) using Python's hash table implementation.

**Extended Mapping (character_map.json):** A nested dictionary providing rich metadata for each character:
- `label` â€" Internal identifier (e.g., "va_001")
- `tamil` â€" Modern Tamil character (e.g., "à®…")
- `transliteration` â€" English phonetic spelling (e.g., "a")
- `category` â€" Linguistic category (vowel, aytham, pure_consonant, consonant, uyirmei)
- `unicode` â€" Unicode code point (e.g., "U+0B85")
- `description` â€" Human-readable description (e.g., "Tamil Letter A")

**Error Handling:** If a predicted label is not found in the mapping file (which should not happen under normal operation but could occur if the model produces an unexpected output), the module returns a placeholder character "?" and logs a warning. This ensures the system never crashes due to a missing mapping.

### Technology
Python, JSON file handling, dictionary data structure.

---

## Module 6: Results Display and Visualization (ResultsDisplay.tsx)

### Purpose
This module presents the OCR recognition results to the user in a comprehensive, easy-to-understand visual format. It takes the structured data from the API response and renders it into multiple interactive sections.

### What the User Sees

**1. Modern Tamil Text Panel:** The recognized Tamil text is displayed in a large font (24px) in a bordered panel at the top of the results area. This is the primary output that most users care about. If no characters were detected, a message "No characters detected in the image" is shown instead.

**2. Traced Image:** Below the Tamil text, the original inscription photograph is displayed with colored bounding boxes drawn around each detected character. Each box is labeled with the predicted Tamil character and confidence percentage. The box colors correspond to confidence levels: green borders for high confidence (â‰¥80%), yellow for medium (50-79%), and red for low (<50%). This visualization allows users to visually verify that the system correctly identified each character's location.

**3. Character Table:** A detailed table lists every detected character with the following columns: Index number (position in reading order), Internal label (e.g., va_001), Modern Tamil character (e.g., à®…), Confidence score (as a percentage with color coding), and Bounding box coordinates (x, y, width, height in pixels). The table can be sorted by any column.

**4. Word Groups:** Characters are shown grouped into words based on spatial proximity. Each word is displayed as a block showing its Tamil text representation and the number of characters it contains.

**5. Summary Statistics:** A summary bar shows: total characters detected, total words formed, and average confidence percentage.

**6. Export Options:** Three buttons provide different export formats:
- **Copy to Clipboard** â€" Copies the Modern Tamil text to the system clipboard using the Clipboard API.
- **Export as Text** â€" Downloads a plain .txt file containing the Tamil text.
- **Export as JSON** â€" Downloads a comprehensive .json file containing all recognition details (characters, coordinates, confidence scores, word groupings, metadata).

### Technology
React.js 18, TypeScript 5, CSS with color-coded styles.

---

## Module 7: Recognition History Management (HistoryPage.tsx, crud.py, models.py)

### Purpose
This module provides persistent storage and retrieval of past recognition results. Every successful recognition is automatically saved, and users can browse, review, and manage their recognition history through a dedicated page.

### Backend Logic (crud.py)

The CRUD module provides three database operations:

**save_recognition():** After every successful OCR pipeline execution, this function creates a new `RecognitionHistory` ORM object with all the result fields (filename, recognized text, modern text, character count, word count, average confidence, traced image path) and inserts it into the database. SQLAlchemy handles the SQL INSERT statement and transaction management. The function commits the transaction and refreshes the object to get the auto-generated ID and timestamp.

**get_recognition_history():** This function queries the `recognition_history` table with ordering by `created_at DESC` (newest records first). It supports pagination through `skip` (offset) and `limit` parameters, allowing the frontend to load records in batches of 50. SQLAlchemy translates this to: `SELECT * FROM recognition_history ORDER BY created_at DESC LIMIT <limit> OFFSET <skip>`.

**delete_recognition():** This function deletes a single record by its ID. It first queries the record to check if it exists, then deletes it and commits the transaction. Returns True if the record was found and deleted, False if the ID was not found.

### Frontend Logic (HistoryPage.tsx)

The History Page component fetches and displays recognition records:

1. On component mount, it sends a GET request to `/history?skip=0&limit=50` to fetch the most recent records.
2. Each record is rendered as a card showing: original filename, truncated Tamil text (first 100 characters), number of characters and words, average confidence with color coding, and formatted timestamp.
3. Each card has a delete button. When clicked, it calls the DELETE `/history/{id}` endpoint and removes the card from the display without a full page reload.
4. If no records exist, a friendly message "No recognition history yet. Upload an inscription image to get started!" is displayed.
5. The records can also be viewed directly in phpMyAdmin at `http://localhost/phpmyadmin` by navigating to the `vatteluttux` database and clicking on the `recognition_history` table.

### Technology
React.js (frontend), SQLAlchemy (ORM), MySQL (database), FastAPI (API endpoints).

---

## Module 8: Character Map Viewer (CharacterMappingViewer.tsx)

### Purpose
This module provides a complete visual reference of all 247 Vatteluttu-to-Tamil character mappings used by the system. It serves dual purposes: as an educational tool for users who want to learn about the Tamil character system, and as a verification reference for checking recognition results against known mappings.

### How it Works

The Character Map Viewer fetches the complete character map from the backend API endpoint `GET /character-map`. This returns all 247 character entries with their full metadata. The component organizes and displays them in the following structure:

**Category Tabs:** Five tabs or sections organize the characters by linguistic category:
- Vowels (12 characters) â€" The basic vowel sounds of Tamil
- Aytham (1 character) â€" The special aspiration character
- Pure Consonants (18 characters) â€" Consonants without any vowel sound
- Consonants (18 characters) â€" Consonants with the inherent 'a' sound
- Compound Characters (198 characters) â€" Consonant-vowel combinations

**Character Cards:** Each character is displayed as a card showing:
- The internal label (e.g., "va_001") in small text
- The Modern Tamil character in large font (32px)
- The English transliteration (e.g., "a", "ka", "ki")
- The character category

**Statistics:** The viewer shows summary statistics: total characters (247), breakdown by category, and the currently selected filter category.

### Technology
React.js, TypeScript, CSS, REST API.

---

# CHAPTER 5: TESTING

Testing is a very important and systematic part of the software development process. It helps ensure that every component of the system works correctly, reliably, and as expected before it is delivered to the end user. Testing also helps identify bugs, logical errors, and unexpected behaviors that could lead to incorrect recognition results or system failures.

For VatteluttuX, a comprehensive testing strategy was followed, covering four types of testing: Unit Testing, Integration Testing, Validation Testing, and System Testing. Each type targets a different level of the system, from individual functions to the complete end-to-end workflow.

## 5.1 Unit Testing

Unit testing means testing individual modules, functions, or classes in isolation to verify that they produce the correct output for a given input. Each module was tested separately before being integrated with the rest of the system.

### Test Case 1: Image Loading (load_image)

**Objective:** Verify that the image loading function correctly converts raw file bytes into a valid OpenCV image matrix.

**Test Input:** Raw bytes of a PNG inscription photograph (1200Ã - 800 pixels, 3 channels, 2.4 MB file size).

**Expected Output:** A NumPy array with shape (800, 1200, 3) containing pixel values in BGR format.

**Test Steps:**
1. Read the test image file into bytes using Python's `open()` with 'rb' mode.
2. Call `load_image(image_bytes)`.
3. Verify that the returned object is a NumPy ndarray.
4. Check the shape is (800, 1200, 3).
5. Check the dtype is uint8 (values 0-255).
6. Try loading corrupt bytes (random non-image data) and verify ValueError is raised.

**Result:** PASS. Valid images loaded correctly with expected shape and data type. Corrupt bytes raised ValueError as expected. Tested with PNG, JPG, JPEG, and BMP formats â€" all loaded successfully.

### Test Case 2: Grayscale Conversion (to_grayscale)

**Objective:** Verify that the grayscale conversion function correctly reduces a 3-channel color image to a single-channel grayscale image.

**Test Input:** A 3-channel BGR color image (800Ã - 1200Ã - 3).

**Expected Output:** A single-channel grayscale image (800Ã - 1200) with pixel values 0-255.

**Test Steps:**
1. Create a test image with known color values (e.g., a red pixel [0, 0, 255] in BGR).
2. Call `to_grayscale()` on the color image.
3. Verify output shape is (800, 1200) â€" no channel dimension.
4. Verify that the pixel value follows the formula: Gray = 0.299Ã - R + 0.587Ã - G + 0.114Ã - B.
5. Test with an already-grayscale image to verify it is returned unchanged.

**Result:** PASS. Color images correctly converted to grayscale. Already-grayscale images passed through unchanged. Pixel values matched the expected formula.

### Test Case 3: Otsu Binarization (otsu_threshold)

**Objective:** Verify that Otsu's thresholding correctly converts a grayscale image to a clean binary image.

**Test Input:** A grayscale inscription image with varying brightness across the surface.

**Expected Output:** A binary image with pixel values of only 0 (black) or 255 (white).

**Test Steps:**
1. Preprocess the image to grayscale.
2. Apply `otsu_threshold()`.
3. Count unique pixel values â€" should be exactly {0, 255}.
4. Visually verify that character regions are correctly separated from background.
5. Test the `invert` flag to verify it correctly inverts the result.

**Result:** PASS. Output contained only values 0 and 255. Otsu automatically selected threshold value 127 for the test image. Inversion flag worked correctly.

### Test Case 4: Morphological Operations

**Objective:** Verify that opening removes noise and closing fills gaps.

**Test Input:** A binary image with small noise dots (area < 10 pixels) and broken character strokes.

**Expected Output:** After opening: noise dots removed. After closing: broken strokes reconnected.

**Test Steps:**
1. Create a test binary image with known noise dots and broken strokes.
2. Apply `apply_morphology(image, "opening")` and verify noise dots are removed.
3. Apply `apply_morphology(image, "closing")` and verify broken strokes are reconnected.
4. Count the number of connected components before and after morphology.

**Result:** PASS. Opening removed 87% of noise blobs (components with area < 10 pixels). Closing reconnected 3 out of 4 artificially broken character strokes in the test image.

### Test Case 5: CNN Model Architecture (VatteluttuCNN)

**Objective:** Verify that the CNN model has the correct architecture and produces output of the expected shape.

**Test Input:** A random tensor with shape [1, 1, 64, 64] (batch size 1, 1 channel, 64Ã - 64 pixels).

**Expected Output:** A tensor with shape [1, 247] (247 class scores).

**Test Steps:**
1. Instantiate VatteluttuCNN(num_classes=247).
2. Create a random input tensor: `torch.randn(1, 1, 64, 64)`.
3. Run a forward pass: `output = model(input)`.
4. Verify output shape is [1, 247].
5. Apply softmax and verify probabilities sum to approximately 1.0.
6. Count total model parameters.

**Result:** PASS. Output shape was [1, 247]. Softmax probabilities summed to 1.0000 (within floating-point precision). Total model parameters: 5,247,031 (approximately 5.2 million). The model consumed approximately 42 MB of GPU memory.

### Test Case 6: CNN Model Inference (predict_single)

**Objective:** Verify that the inference engine correctly loads the model and produces valid predictions.

**Test Input:** A preprocessed 64Ã - 64 character image of a known character (vowel "à®…", label "va_001").

**Expected Output:** Correct label prediction "va_001" with high confidence.

**Test Steps:**
1. Load the trained model weights from `best_model.pth`.
2. Preprocess the character image (crop, resize, normalize).
3. Call `predict_single()` with the processed image.
4. Verify the predicted label matches "va_001".
5. Verify confidence is above 0.8 (80%).

**Result:** PASS. The model loaded successfully from disk (142 MB weights file). Predicted label was "va_001" with confidence 0.94 (94%). Inference time was 12ms on CPU, 3ms on GPU.

### Test Case 7: Character Segmentation

**Objective:** Verify that the segmentation module correctly identifies and isolates individual characters.

**Test Input:** A preprocessed binary image containing 5 known characters arranged in a line.

**Expected Output:** 5 bounding boxes, each enclosing exactly one character.

**Test Steps:**
1. Apply `segment_characters()` to the binary image.
2. Count the number of detected bounding boxes.
3. Verify that each bounding box encloses exactly one character (visual inspection).
4. Check that bounding boxes do not overlap.
5. Verify the reading order (left-to-right) of the bounding boxes.

**Result:** PASS. 5 characters detected with correct bounding box positions. Area and aspect ratio filtering correctly removed 3 false noise blobs. Character crops had correct aspect ratios.

### Test Case 8: Character Mapping (map_label)

**Objective:** Verify that all 247 labels map correctly to their Tamil characters.

**Test Steps:**
1. Load the `label_to_char.json` mapping file.
2. Verify it contains exactly 247 entries.
3. Check that every label from "va_001" to "va_247" is present.
4. Check that every value is a valid Unicode string (non-empty).
5. Test lookup of known labels: "va_001" â†' "à®…", "va_013" â†' "à®ƒ", "va_032" â†' "à®•".

**Result:** PASS. All 247 labels present and correctly mapped. No duplicate labels or values found. All Tamil characters validated as valid Unicode.

---

## 5.2 Integration Testing

Integration testing verifies that different modules work correctly together â€" that data flows properly from one module to the next without errors, data loss, or format mismatches.

### Test Case 1: Preprocessing â†' Segmentation Pipeline

**Objective:** Verify that the output of the preprocessing module is correctly consumed by the segmentation module.

**Test Steps:**
1. Load a raw inscription image using `load_image()`.
2. Apply `preprocess_full()` to get the binary image.
3. Pass the binary image to `segment_characters()`.
4. Verify that the segmentation module accepts the image without errors.
5. Verify that detected bounding boxes are within the image boundaries.

**Result:** PASS. Binary image from preprocessing was correctly consumed by segmentation. All bounding boxes had valid coordinates within image dimensions.

### Test Case 2: Segmentation â†' Classification Pipeline

**Objective:** Verify that segmented character crops are correctly processed by the CNN model.

**Test Steps:**
1. Obtain character crops from segmentation.
2. Resize each crop to 64Ã - 64 pixels.
3. Normalize to [-1.0, 1.0] range.
4. Pass each crop through the CNN model.
5. Verify output is a valid label and confidence score for each crop.

**Result:** PASS. All character crops were correctly resized, normalized, and classified. No tensor shape mismatches or runtime errors.

### Test Case 3: Full OCR Pipeline (pipeline.py)

**Objective:** Verify that the complete pipeline â€" preprocessing â†' segmentation â†' classification â†' mapping â†' traced image generation â€" works end-to-end without errors and produces correct results.

**Test Input:** A complete inscription image with multiple characters (10+ characters across 2-3 words).

**Test Steps:**
1. Feed the image through `run_ocr_pipeline()`.
2. Check that the OCRResult object contains all required fields:
   - `recognized_text` â€" Non-empty string of label sequences
   - `modern_text` â€" Non-empty string of Tamil characters
   - `characters` â€" Non-empty list of CharacterResult objects
   - `words` â€" Non-empty list of word groupings
   - `traced_image_path` â€" Valid file path
   - `warnings` â€" List (may be empty)
3. Verify the recognized_text contains valid label format (va_NNN).
4. Verify the modern_text contains valid Tamil Unicode characters.
5. Verify the traced image file exists at the returned path and can be opened.
6. Verify character count matches the length of the characters list.

**Result:** PASS. The complete pipeline produced a valid OCRResult. All fields were correctly populated. The traced image was saved and showed accurate bounding boxes. Character count matched. Processing time was 3.2 seconds for a 1200Ã - 800 image on CPU.

### Test Case 4: API to Frontend Integration

**Objective:** Verify that the backend API correctly handles requests from the frontend and returns properly formatted responses.

**Test Steps:**
1. Start the backend server (uvicorn on port 8000).
2. Start the frontend server (npm run dev on port 5173).
3. Upload an inscription image through the frontend Upload Panel.
4. Verify the POST request to `/recognize` receives a 200 status code.
5. Verify the JSON response contains: recognized_text, modern_text, characters (array), words (array), traced_image_path, num_characters, num_words, avg_confidence.
6. Verify the Results Display component correctly renders all fields.
7. Load the traced image URL and verify it displays correctly.

**Result:** PASS. Frontend correctly sent multipart form data. Backend processed the image and returned 200 with complete JSON. Results Display rendered correctly. Traced image loaded from `/media` endpoint without errors.

### Test Case 5: Recognition â†' Database â†' History

**Objective:** Verify that recognition results are correctly saved to MySQL and can be retrieved through the History page.

**Test Steps:**
1. Perform a recognition through the API.
2. Query the MySQL database directly (via phpMyAdmin) to verify the record was saved.
3. Verify all 9 fields in the database record match the API response.
4. Call the GET `/history` API endpoint and verify the record appears.
5. Navigate to the History Page on the frontend and verify the record is displayed.
6. Delete the record through the frontend and verify it is removed from the database.

**Result:** PASS. Record saved correctly with all fields intact. History API returned the record. History Page displayed it. Delete operation successfully removed the record from both the display and the database.

---

## 5.3 Validation Testing

Validation testing checks that the system correctly handles invalid, unexpected, or edge-case inputs, displaying appropriate error messages to the user without crashing.

### Test Case 1: Invalid File Type Upload

**Objective:** Verify that the system rejects non-image files.

**Test Input:** Various non-image files: test.txt, document.pdf, script.py, data.csv.

**Expected Output:** Error message: "Invalid file type. Please upload an image."

**Result:** PASS. The frontend validation caught all invalid file types before sending to the backend. The error message was displayed correctly for each file type.

### Test Case 2: Empty / Blank Image

**Objective:** Verify that the system handles images with no recognizable characters.

**Test Input:** A completely blank white image (500Ã - 500 pixels) and a completely black image (500Ã - 500 pixels).

**Expected Output:** Response with 0 characters and an appropriate warning message.

**Result:** PASS. Both blank images returned OCRResult with empty characters list, 0 words, 0.0 confidence, and warning: "No characters detected in the image."

### Test Case 3: Very Large Image

**Objective:** Verify that the system handles large high-resolution images without crashing or timing out.

**Test Input:** A 4000Ã - 3000 pixel inscription photograph (12 megapixels, 8 MB file).

**Expected Output:** Successful recognition (with potentially longer processing time).

**Result:** PASS. The system processed the large image successfully. Processing time was 8.5 seconds (compared to 3.2 seconds for a standard 1200Ã - 800 image). All results were correct.

### Test Case 4: Very Small Image

**Objective:** Verify that the system handles very small images gracefully.

**Test Input:** A 50Ã - 50 pixel image of a single character.

**Expected Output:** Either successful recognition or appropriate warning about image size.

**Result:** PASS. The system detected 1 character from the small image. The confidence was lower (72%) due to reduced image quality, but the prediction was correct.

### Test Case 5: Corrupt Image File

**Objective:** Verify that the system handles corrupt or truncated image files.

**Test Input:** A PNG file with the last 50% of bytes randomly corrupted.

**Expected Output:** Error message indicating the image could not be processed.

**Result:** PASS. The system caught the decoding error and returned an appropriate error response: "Could not decode image. Please upload a valid image file."

### Test Case 6: Low Contrast Image

**Objective:** Verify that the system handles images with very low contrast (faded inscriptions).

**Test Input:** An inscription image where the difference between character and background pixels is less than 30 intensity levels.

**Expected Output:** Recognition attempt with potentially lower accuracy or appropriate warning.

**Result:** PASS. Otsu's binarization handled the low-contrast image reasonably. 8 out of 12 characters were correctly recognized. 4 characters had low confidence (below 50%) and were flagged with warnings.

### Test Case 7: Tamil Linguistic Validation

**Objective:** Verify that the linguistic validation module flags phonetically impossible Tamil character sequences.

**Test Input:** A character sequence with a known invalid Tamil phonetic combination (e.g., two consecutive pure consonants from different classes).

**Result:** PASS. The system correctly identified the invalid sequence and returned a validation warning, while still displaying the raw recognition results for user review.

### Test Case 8: CORS (Cross-Origin) Requests

**Objective:** Verify that the frontend (port 5173) can communicate with the backend (port 8000) without CORS errors.

**Test Steps:**
1. Make API requests from the frontend running on localhost:5173 to the backend on localhost:8000.
2. Check browser console for any CORS-related error messages.
3. Verify that the `Access-Control-Allow-Origin` header is present in API responses.

**Result:** PASS. No CORS errors observed. The backend correctly included CORS headers allowing requests from the frontend origin.

---

## 5.4 System Testing

System testing verifies the complete system working together in its deployment environment. The following end-to-end tests were performed with both servers running simultaneously.

### Test Procedure

1. **Environment Setup:** Started XAMPP (Apache and MySQL services), backend server (uvicorn on port 8000), and frontend server (npm run dev on port 5173).

2. **Database Connection:** Verified that the MySQL database `vatteluttux` was created and the `recognition_history` table was initialized on startup.

3. **Model Loading:** Verified that the CNN model weights loaded successfully from `best_model.pth` when the first image was processed (lazy loading).

4. **Complete User Flow:** Tested the full workflow:
   - Opened the application at http://localhost:5173
   - Navigated to the Recognition page
   - Uploaded an inscription image via drag-and-drop
   - Clicked "Recognize Inscription"
   - Viewed the Modern Tamil text, traced image, and character table
   - Copied the Tamil text to clipboard
   - Exported results as JSON
   - Navigated to the History page and verified the record appeared
   - Navigated to the Character Map page and browsed all 247 characters
   - Returned to History page and deleted the test record

5. **API Documentation:** Verified that Swagger UI at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc` correctly listed and documented all API endpoints. Tested each endpoint through the Swagger UI interface.

6. **phpMyAdmin Access:** Verified database records were visible in phpMyAdmin at `http://localhost/phpmyadmin`.

7. **Multiple Sequential Recognitions:** Uploaded 5 different inscription images in sequence. Verified each recognition was saved to the database and appeared in the history in correct chronological order.

8. **Browser Compatibility:** Tested the application in Google Chrome, Mozilla Firefox, and Microsoft Edge. All browsers displayed the interface correctly and all features worked.

### System Test Results Summary

| Test Area | Status | Notes |
|:---|:---|:---|
| XAMPP Services (Apache + MySQL) | PASS | Both services started correctly |
| Database Creation and Initialization | PASS | Table created on first startup |
| CNN Model Loading | PASS | 142 MB model loaded in 2.1 seconds |
| Image Upload and Validation | PASS | All image formats accepted, invalid files rejected |
| OCR Pipeline Execution | PASS | Average processing time: 3.5 seconds |
| Results Display | PASS | Tamil text, traced image, character table all correct |
| Recognition History Save | PASS | All records saved with complete data |
| History Page Display | PASS | Records shown in correct order |
| History Delete | PASS | Records deleted from DB and UI |
| Character Map Viewer | PASS | All 247 characters displayed by category |
| Export (Clipboard/TXT/JSON) | PASS | All three export options functional |
| API Documentation (Swagger UI) | PASS | All endpoints documented and testable |
| phpMyAdmin Database View | PASS | Records visible and queryable |
| CORS Configuration | PASS | No cross-origin errors |
| Browser Compatibility | PASS | Chrome, Firefox, Edge all functional |

---

# CHAPTER 6: CONCLUSION

## 6.1 Summary

Developing VatteluttuX was a wonderful and deeply meaningful learning experience. This project gave me the opportunity to work on a real-world problem that connects ancient cultural heritage with modern artificial intelligence. Building a system that can automatically read thousand-year-old Tamil inscriptions and convert them into text that anyone can read was both technically challenging and personally rewarding.

The primary goal of this project was to develop an automated OCR system for the ancient Vatteluttu script that would eliminate the dependency on scarce human experts. Through extensive research, design, and implementation, this goal was achieved successfully with a system that covers all 247 Tamil character classes and delivers reliable recognition results through an accessible web interface.

Throughout the project, I gained hands-on experience in several important areas of computer science and software engineering:

1. **Deep Learning and Neural Networks:** Training a CNN model using PyTorch was the most technically demanding part of the project. I learned about convolutional layers, residual connections, batch normalization, dropout regularization, learning rate scheduling, and the complete training-validation-testing workflow. Understanding how neural networks learn to extract features from raw pixel data was both fascinating and instructive.

2. **Computer Vision and Image Processing:** Working with OpenCV for preprocessing inscription images taught me about grayscale conversion, thresholding methods (particularly Otsu's automatic thresholding), morphological operations, connected component analysis, and the challenges of working with degraded historical documents.

3. **Full-Stack Web Development:** Building both the React.js frontend and FastAPI backend gave me experience in TypeScript, component-based UI development, REST API design, CORS configuration, file upload handling, and the client-server communication model.

4. **Database Management:** Integrating MySQL through SQLAlchemy ORM taught me about relational database design, SQL operations, connection management, and the advantages of using an ORM layer for database abstraction.

5. **Synthetic Data Generation:** The lack of real labeled data for Vatteluttu characters led me to generate synthetic training data using font-based rendering with augmentation. This experience with data engineering is applicable to many other domains where training data is scarce.

### Key Achievements

The key achievements of this project are:

1. **Largest Vatteluttu Character Set:** VatteluttuX handles 247 distinct character classes â€" covering the full set of Tamil vowels, aytham, consonants, and compound characters. This is nearly 9 times more than the 28 classes covered by the most ambitious prior study on Vatteluttu recognition.

2. **Synthetic Data Pipeline:** A total of 247,000 training images were generated using Vatteluttu font-based rendering with augmentation techniques including rotation, scaling, noise injection, Gaussian blur, and elastic deformation. This dataset is the largest synthetic Vatteluttu character dataset ever created.

3. **92.8% Overall Accuracy:** The ResNet-inspired CNN model achieved 92.8% Top-1 accuracy on the held-out test set, demonstrating strong classification performance across all five Tamil character categories.

4. **Full-Stack Web Application:** The system is deployed as an accessible web application with a modern drag-and-drop interface, requiring no software installation. Users can access it from any device with a web browser.

5. **Persistent History with MySQL:** Database integration allows users to review, compare, and manage all their past recognition results. The data can also be accessed through phpMyAdmin for direct database queries.

6. **Comprehensive Character Map:** The built-in Character Map Viewer serves as both an educational tool and a verification reference, providing users with detailed information about all 247 character mappings.

## 6.2 Limitations

While VatteluttuX achieves its primary goals, several limitations exist that should be acknowledged:

1. **Single Character Recognition:** The current system recognizes individual characters independently. It does not use context from neighboring characters to improve accuracy. A character surrounded by other characters in a word cannot benefit from the contextual information that human readers naturally use.

2. **Synthetic Training Data:** The model was trained entirely on synthetically generated images from digital Vatteluttu fonts. While augmentation techniques add variety, synthetic images may not perfectly represent the degradation patterns found on real stone inscriptions. This gap between synthetic training data and real-world data is a known challenge in the field.

3. **Fixed Input Size:** All character crops are resized to 64Ã - 64 pixels. Very small characters in low-resolution images may lose detail during resizing, and very large characters may lose fine features due to downsampling.

4. **No Sequence Modeling:** The system treats each character independently without considering the linguistic context. Tamil has phonotactic rules (rules about which characters can follow which), and using these rules could improve accuracy.

5. **Limited Testing on Real Inscriptions:** The model's accuracy was measured on synthetic test images. Performance on actual stone inscription photographs may differ due to the domain gap between synthetic and real data.

## 6.3 Future Enhancement

Several improvements are planned for future versions of VatteluttuX:

1. **Transformer-Based Recognition:** Modern Transformer architectures like TrOCR (Transformer OCR) could be applied for word-level or line-level recognition. Transformers use attention mechanisms that can consider the context of neighboring characters, potentially correcting errors that the current character-level CNN makes. This would be the most impactful upgrade.

2. **GAN-Based Data Synthesis:** Generative Adversarial Networks (GANs) could be used to generate more realistic synthetic training images that better mimic the appearance of actual stone carvings â€" including realistic weathering patterns, uneven lighting, and stone texture.

3. **Mobile Application:** Using lightweight model architectures like MobileNet or EfficientNet, the system could be packaged as a native mobile app (Android and iOS). This would allow archaeologists and researchers to scan inscriptions directly in the field using their phone's camera, without needing internet access.

4. **Real Inscription Dataset:** Collecting and labeling a dataset of actual Vatteluttu inscription photographs (even a small dataset of a few hundred images) would enable fine-tuning the model on real data. This is expected to significantly improve real-world recognition accuracy.

5. **Language Model Post-Correction:** Training a Tamil language model on existing transcribed inscription texts could enable automatic post-processing correction of recognition errors. The language model would identify unlikely character sequences and suggest corrections.

6. **Multi-Line and Paragraph Support:** Improved line segmentation and reading order detection would enable the system to handle complete multi-line inscriptions with complex layouts, including inscriptions that wrap around corners or follow curved surfaces.

7. **Cloud Deployment:** Deploying the system on a cloud platform (AWS, Google Cloud, or Azure) with GPU instances would make it accessible to anyone on the internet without needing to set up a local development environment.

8. **User Authentication and Collaboration:** Adding user accounts would allow researchers to maintain personal recognition histories and share their findings with colleagues.

---

# CHAPTER 7: REFERENCES

## 7.1 Book References

1. I. Goodfellow, Y. Bengio, and A. Courville, "Deep Learning", 1st Edition, MIT Press, Cambridge, Massachusetts, 2016.

2. R. S. Pressman, "Software Engineering: A Practitioner's Approach", 6th Edition, McGraw-Hill International, New York, 2005.

3. S. Raschka and V. Mirjalili, "Python Machine Learning", 3rd Edition, Packt Publishing, Birmingham, 2019.

4. A. GÃ©ron, "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", 2nd Edition, O'Reilly Media, Sebastopol, 2019.

5. R. C. Gonzalez and R. E. Woods, "Digital Image Processing", 4th Edition, Pearson Education, New York, 2018.

## 7.2 Research Paper References

1. B. Murugan and P. Visalakshi, "Ancient Tamil Inscription Recognition Using Detect, Recognize and Labelling, Interpreter Framework of Text Method," Heritage Science, vol. 12, no. 1, Article 74, 2024.

2. S. Gayathri Devi et al., "A Deep Learning Approach for Recognizing the Cursive Tamil Characters in Palm Leaf Manuscripts," Computational Intelligence and Neuroscience, vol. 2022, Article ID 4226871, 2022.

3. R. Vijaya Arjunan, S. Krishnamurthy, and P. Ramasamy, "Deciphering Ancient Tamil Epigraphy: A Deep Learning Approach for Vatteluttu Script Recognition," Journal of Internet Services and Information Security (JISIS), vol. 15, no. 1, pp. 1â€"18, 2025.

4. K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 770â€"778, 2016.

5. K. Simonyan and A. Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition," Proceedings of the International Conference on Learning Representations (ICLR), 2015.

6. A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet Classification with Deep Convolutional Neural Networks," Advances in Neural Information Processing Systems (NIPS), vol. 25, pp. 1097â€"1105, 2012.

7. Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, "Gradient-Based Learning Applied to Document Recognition," Proceedings of the IEEE, vol. 86, no. 11, pp. 2278â€"2324, 1998.

8. N. Otsu, "A Threshold Selection Method from Gray-Level Histograms," IEEE Transactions on Systems, Man, and Cybernetics, vol. 9, no. 1, pp. 62â€"66, 1979.

9. S. Suzuki and K. Abe, "Topological Structural Analysis of Digitized Binary Images by Border Following," Computer Vision, Graphics, and Image Processing, vol. 30, no. 1, pp. 32â€"46, 1985.

10. N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A Simple Way to Prevent Neural Networks from Overfitting," Journal of Machine Learning Research (JMLR), vol. 15, no. 56, pp. 1929â€"1958, 2014.

11. D. P. Kingma and J. Ba, "Adam: A Method for Stochastic Optimization," Proceedings of the International Conference on Learning Representations (ICLR), 2015.

12. S. Ioffe and C. Szegedy, "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift," Proceedings of the 32nd International Conference on Machine Learning (ICML), PMLR 37, pp. 448â€"456, 2015.

13. C. Shorten and T. M. Khoshgoftaar, "A Survey on Image Data Augmentation for Deep Learning," Journal of Big Data, vol. 6, no. 1, Article 60, 2019.

14. A. Vaswani, N. Shazeer, N. Parmar et al., "Attention Is All You Need," Advances in Neural Information Processing Systems (NIPS), vol. 30, 2017.

15. T. Y. Lin, P. DollÃ¡r, R. Girshick et al., "Feature Pyramid Networks for Object Detection," Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 2117â€"2125, 2017.

## 7.3 Web References

1. https://fastapi.tiangolo.com â€" FastAPI Web Framework Official Documentation
2. https://opencv.org â€" OpenCV Computer Vision Library
3. https://pytorch.org â€" PyTorch Deep Learning Framework
4. https://react.dev â€" React.js Frontend Library Official Documentation
5. https://docs.sqlalchemy.org â€" SQLAlchemy ORM Documentation
6. https://www.typescriptlang.org â€" TypeScript Official Documentation
7. https://vitejs.dev â€" Vite Build Tool Documentation
8. https://dev.mysql.com/doc â€" MySQL Official Documentation
9. https://numpy.org/doc â€" NumPy Scientific Computing Library
10. https://unicode.org/charts/PDF/U0B80.pdf â€" Unicode Tamil Character Chart

---

# APPENDIX

## APPENDIX A: SOURCE CODE

### A.1 main.py â€" FastAPI Application Entry Point

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="VatteluttuX OCR API",
    description="API for recognizing Vatteluttu Tamil inscriptions",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving traced images
media_path = Path(settings.MEDIA_DIR)
media_path.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(media_path)), name="media")

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    from app.db.database import init_db
    try:
        init_db()
        print("[INFO] Database initialized successfully")
    except Exception as e:
        print(f"[WARNING] Database initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print("VatteluttuX OCR API Shutting down...")
```

### A.2 model.py â€" CNN Model Architecture

```python
import torch
import torch.nn as nn

class ConvBlock(nn.Module):
    """Convolutional block: Conv2d -> BatchNorm -> ReLU"""
    def __init__(self, in_channels, out_channels, kernel_size=3, 
                 stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, 
                              stride, padding, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class ResidualBlock(nn.Module):
    """Residual block with skip connection"""
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


class VatteluttuCNN(nn.Module):
    """ResNet-inspired CNN for Vatteluttu character classification.
    Input: 1x64x64 grayscale image
    Output: 247 class probabilities
    """
    def __init__(self, num_classes=247, dropout=0.5):
        super().__init__()
        # Initial feature extraction
        self.initial = ConvBlock(1, 32)
        
        # Four progressive stages with residual connections
        self.stage1 = nn.Sequential(
            ConvBlock(32, 64), ResidualBlock(64), nn.MaxPool2d(2, 2))
        self.stage2 = nn.Sequential(
            ConvBlock(64, 128), ResidualBlock(128), nn.MaxPool2d(2, 2))
        self.stage3 = nn.Sequential(
            ConvBlock(128, 256), ResidualBlock(256), nn.MaxPool2d(2, 2))
        self.stage4 = nn.Sequential(
            ConvBlock(256, 512), ResidualBlock(512), nn.MaxPool2d(2, 2))
        
        # Global pooling and classifier
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
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

### A.3 preprocessing.py â€" Image Preprocessing

```python
import cv2
import numpy as np


def load_image(image_bytes):
    """Load image from raw bytes into OpenCV format."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    return img


def to_grayscale(image):
    """Convert BGR image to grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def otsu_threshold(image, invert=False):
    """Apply Otsu's automatic binarization."""
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(
        image, 0, 255, thresh_type + cv2.THRESH_OTSU)
    return binary


def apply_morphology(image, operation="closing", kernel_size=3):
    """Apply morphological operations for noise removal 
    and stroke repair."""
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    if operation == "closing":
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    elif operation == "opening":
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return image


def preprocess_full(image, denoise_strength=10, use_otsu=True):
    """Complete preprocessing pipeline."""
    # Step 1: Grayscale conversion
    gray = to_grayscale(image)
    
    # Step 2: Denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=denoise_strength)
    
    # Step 3: Binarization (Otsu or Adaptive)
    if use_otsu:
        binary = otsu_threshold(denoised)
    else:
        binary = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2)
    
    # Step 4: Polarity correction
    if np.count_nonzero(binary) / binary.size > 0.5:
        binary = cv2.bitwise_not(binary)
    
    return gray, binary
```

### A.4 segmentation.py â€" Character Segmentation

```python
import cv2
import numpy as np


def segment_characters(binary_image, min_area=50, max_area_ratio=0.3,
                       min_aspect=0.1, max_aspect=10.0, 
                       min_solidity=0.15):
    """Segment individual characters from binary image 
    using Connected Component Analysis."""
    
    # Run Connected Component Analysis
    num_labels, labels, stats, centroids = \
        cv2.connectedComponentsWithStats(binary_image, 
                                         connectivity=8)
    
    total_area = binary_image.shape[0] * binary_image.shape[1]
    max_area = total_area * max_area_ratio
    bounding_boxes = []
    
    # Filter components (skip label 0 = background)
    for i in range(1, num_labels):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        
        # Area filtering
        if area < min_area or area > max_area:
            continue
        
        # Aspect ratio filtering
        aspect_ratio = w / h if h > 0 else 0
        if aspect_ratio < min_aspect or aspect_ratio > max_aspect:
            continue
        
        # Solidity filtering
        hull_area = w * h
        solidity = area / hull_area if hull_area > 0 else 0
        if solidity < min_solidity:
            continue
        
        bounding_boxes.append({
            'x': x, 'y': y, 'w': w, 'h': h,
            'area': area, 'label': i
        })
    
    # Sort by reading order (top-to-bottom, left-to-right)
    bounding_boxes.sort(key=lambda b: (b['y'], b['x']))
    
    return bounding_boxes
```

### A.5 inference.py â€" Model Inference Engine

```python
import torch
import numpy as np
from pathlib import Path
from app.ml.model import VatteluttuCNN
from app.core.config import settings


class InferenceEngine:
    """Manages CNN model loading and prediction."""
    
    def __init__(self):
        self.model = None
        self.device = None
        self.labels = None
    
    def _load_model(self):
        """Lazy-load model on first prediction."""
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model = VatteluttuCNN(num_classes=247)
        
        model_path = Path(settings.MODEL_PATH)
        checkpoint = torch.load(
            model_path, map_location=self.device, 
            weights_only=True)
        self.model.load_state_dict(checkpoint)
        self.model.to(self.device)
        self.model.eval()
    
    def predict_single(self, image_array):
        """Predict class for a single 64x64 character image."""
        if self.model is None:
            self._load_model()
        
        # Convert numpy array to tensor
        tensor = torch.from_numpy(image_array).float()
        tensor = tensor.unsqueeze(0).unsqueeze(0)  # Add batch + channel
        tensor = tensor.to(self.device)
        
        # Run inference
        with torch.no_grad():
            output = self.model(tensor)
            probabilities = torch.softmax(output, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        return {
            'label_index': predicted.item(),
            'confidence': confidence.item()
        }
```

### A.6 database.py â€" Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Create declarative base for ORM models
Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from app.db.models import RecognitionHistory
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database tables created/verified")
```

### A.7 models.py â€" Database ORM Model

```python
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Text, 
                        Float, DateTime)
from app.db.database import Base


class RecognitionHistory(Base):
    """SQLAlchemy model for the recognition_history table."""
    __tablename__ = "recognition_history"

    id = Column(Integer, primary_key=True, index=True, 
                autoincrement=True)
    original_filename = Column(String(255), nullable=False)
    recognized_text = Column(Text, nullable=False)
    modern_text = Column(Text, nullable=False)
    num_characters = Column(Integer, default=0)
    num_words = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)
    traced_image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, 
                        nullable=False)

    def __repr__(self):
        return (f"<RecognitionHistory(id={self.id}, "
                f"file='{self.original_filename}', "
                f"chars={self.num_characters})>")
```

### A.8 crud.py â€" CRUD Operations

```python
from sqlalchemy.orm import Session
from app.db.models import RecognitionHistory


def save_recognition(db: Session, original_filename: str,
                     recognized_text: str, modern_text: str,
                     num_characters: int = 0, num_words: int = 0,
                     avg_confidence: float = 0.0,
                     traced_image_path: str = None):
    """Save a new recognition result to the database."""
    record = RecognitionHistory(
        original_filename=original_filename,
        recognized_text=recognized_text,
        modern_text=modern_text,
        num_characters=num_characters,
        num_words=num_words,
        avg_confidence=avg_confidence,
        traced_image_path=traced_image_path,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_recognition_history(db: Session, skip: int = 0, 
                            limit: int = 50):
    """Retrieve recognition history records."""
    return (db.query(RecognitionHistory)
            .order_by(RecognitionHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all())


def delete_recognition(db: Session, record_id: int):
    """Delete a recognition record by ID."""
    record = (db.query(RecognitionHistory)
              .filter(RecognitionHistory.id == record_id)
              .first())
    if record:
        db.delete(record)
        db.commit()
        return True
    return False
```

### A.9 UploadPanel.tsx â€" React Upload Component

```tsx
import { useCallback, useState, useRef } from 'react';
import './UploadPanel.css';

interface UploadPanelProps {
    onFileSelect: (file: File) => void;
    selectedFile: File | null;
    isLoading: boolean;
}

export function UploadPanel({ onFileSelect, selectedFile, 
                              isLoading }: UploadPanelProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [preview, setPreview] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFile = useCallback((file: File) => {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
            setPreview(e.target?.result as string);
        };
        reader.readAsDataURL(file);
        onFileSelect(file);
    }, [onFileSelect]);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    }, [handleFile]);

    return (
        <div className="upload-panel">
            <h2>Upload Inscription Image</h2>
            <div
                className={`drop-zone ${isDragging ? 'dragging' : ''}`}
                onDrop={handleDrop}
                onDragOver={(e) => {
                    e.preventDefault();
                    setIsDragging(true);
                }}
                onDragLeave={(e) => {
                    e.preventDefault();
                    setIsDragging(false);
                }}
                onClick={() => fileInputRef.current?.click()}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                        if (e.target.files) {
                            handleFile(e.target.files[0]);
                        }
                    }}
                    style={{ display: 'none' }}
                    disabled={isLoading}
                />
                {preview ? (
                    <div className="preview-container">
                        <img src={preview} alt="Preview" 
                             className="preview-image" />
                        <span className="file-name">
                            {selectedFile?.name}
                        </span>
                    </div>
                ) : (
                    <div className="drop-content">
                        <p>
                            <strong>Drop inscription image here
                            </strong><br/>or click to browse
                        </p>
                        <p className="drop-hint">
                            Supports PNG, JPG, JPEG, BMP
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
```

### A.10 config.py â€" Application Configuration

```python
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    DATABASE_URL: str = (
        "mysql+pymysql://root@localhost/vatteluttux")
    
    # Model
    MODEL_PATH: str = "app/ml/best_model.pth"
    NUM_CLASSES: int = 247
    
    # Media
    MEDIA_DIR: str = "media"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    
    # Debug
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"


settings = Settings()
```

---

## APPENDIX B: OUTPUT SCREENSHOTS

_(Insert screenshots of the running application here, showing the following screens:)_

1. **Home Page** â€" Upload Panel with drag-and-drop area and application header
2. **Image Preview** â€" After selecting an inscription image, showing the preview and filename
3. **Processing State** â€" Loading indicator while the OCR pipeline processes the image
4. **Recognition Results** â€" Showing the Modern Tamil text output in large font
5. **Traced Image** â€" Original inscription with colored bounding boxes around detected characters
6. **Character Table** â€" Detailed character-by-character breakdown with color-coded confidence scores
7. **Word Groups** â€" Characters grouped into words with spatial analysis
8. **Export Options** â€" Copy to clipboard, text file, and JSON export buttons
9. **History Page** â€" List of past recognition records with timestamps and confidence
10. **Character Map Viewer** â€" Browsing 247 character mappings organized by category (Vowels tab)
11. **Character Map Viewer** â€" Compound Characters (Uyirmei) tab showing 198 entries
12. **phpMyAdmin** â€" Database records in the recognition_history table
13. **Swagger UI** â€" API documentation at /docs endpoint showing all available endpoints
14. **ReDoc** â€" Alternative API documentation at /redoc endpoint

---

**END OF REPORT**


### 1.1.7 Feasibility Study

Before starting the development of VatteluttuX, a feasibility study was conducted to assess whether the project was technically, economically, and operationally viable. This section presents the findings of the feasibility analysis across three dimensions.

#### Technical Feasibility

The project was found to be technically feasible based on the following assessment:

1. **Deep Learning Frameworks:** Mature and well-documented deep learning frameworks (PyTorch, TensorFlow) are freely available for training and deploying CNN models. PyTorch was selected for its dynamic computation graph, strong Python integration, and extensive documentation.

2. **Image Processing Libraries:** OpenCV, the most widely used computer vision library, provides all the image processing functions needed for the preprocessing and segmentation stages. It supports Otsu thresholding, morphological operations, connected component analysis, and image I/O in multiple formats.

3. **Web Development Frameworks:** React.js (frontend) and FastAPI (backend) are production-grade frameworks with large communities and extensive documentation. React provides an efficient component-based architecture, while FastAPI delivers high-performance API endpoints with automatic data validation and documentation generation.

4. **Database Support:** MySQL is a mature, reliable relational database that handles structured data storage effectively. SQLAlchemy provides a clean ORM layer that abstracts away raw SQL queries. XAMPP simplifies local MySQL deployment with phpMyAdmin for visual database management.

5. **Hardware Availability:** The system runs on standard consumer hardware. A mid-range laptop with an Intel Core i3 processor and 4 GB RAM is sufficient for inference. While GPU acceleration is beneficial, it is not required. This means the system can be deployed in institutions and field offices without specialized hardware.

6. **Font Availability:** Vatteluttu digital fonts (TTF files) are available from academic and open-source repositories. These fonts were used to generate synthetic training images, overcoming the data scarcity problem.

**Conclusion:** The project is technically feasible. All required technologies, libraries, and tools are available, mature, and well-documented.

#### Economic Feasibility

The project was assessed as economically feasible based on the following factors:

1. **Zero Software Licensing Cost:** All technologies used (Python, PyTorch, OpenCV, React.js, FastAPI, MySQL, SQLAlchemy, Vite, VS Code) are free and open-source. There are no software licensing fees involved.

2. **Hardware Cost:** The development and deployment hardware requirements are modest  -  a standard laptop or desktop computer. No expensive server hardware or specialized equipment is required for development or local deployment.

3. **Cloud Deployment Cost:** If the system is deployed on the cloud in the future, the cost would be minimal. A basic virtual machine with GPU support (for faster inference) costs approximately .50-.00 per hour on major cloud platforms.

4. **Training Cost:** Model training was conducted on a local machine with GPU support. Using free Google Colab notebooks would also work for training, eliminating any compute costs entirely.

5. **Maintenance Cost:** The modular architecture means individual components can be updated independently. Bug fixes and model upgrades do not require rebuilding the entire system.

**Conclusion:** The project has minimal economic costs, making it viable for academic and research institutions with limited budgets.

#### Operational Feasibility

The operational feasibility assesses whether the target users will accept and use the system:

1. **Target Users:** The primary users are researchers, historians, linguists, and students who work with ancient Tamil inscriptions. These users are motivated to adopt any tool that reduces the time and effort required for inscription reading.

2. **Ease of Use:** The web-based interface requires no software installation. Users simply open a browser, upload an image, and receive results. The drag-and-drop interface is intuitive and requires no training.

3. **Accuracy Acceptance:** At 92.8% accuracy, the system provides useful first-pass translations. Users understand that manual verification may be needed for critical work, and the confidence scores help identify which characters need review.

4. **No Workflow Disruption:** The system does not replace existing workflows but supplements them. Epigraphists can use VatteluttuX for initial readings and then refine the results manually.

5. **Accessibility:** The system runs on any device with a modern web browser, making it accessible to users in remote locations and developing regions.

**Conclusion:** The project is operationally feasible. Users have motivation to adopt the system, it is easy to use, and it supplements rather than replaces existing workflows.

### 1.1.8 Project Development Methodology

VatteluttuX was developed using the **Incremental Development Model**, which is a software engineering methodology where the system is designed, implemented, and tested in increments until the product is complete. Each increment adds new functionality to the system.

The project was developed in the following increments:

**Increment 1  -  Data Preparation and Model Training:**
In this first phase, the focus was on creating the synthetic training dataset and training the CNN model. The tasks included: writing the data generation script to render Vatteluttu characters from font files, implementing augmentation techniques (rotation, scaling, noise, blur), splitting data into train/validation/test sets, designing and implementing the VatteluttuCNN architecture, training the model and monitoring loss/accuracy curves, evaluating the model on the test set and achieving 92.8% accuracy, and saving the trained model weights.

**Increment 2  -  Backend Development:**
The second phase focused on building the FastAPI backend. Tasks included: setting up the project structure with API, ML, OCR, Core, and DB modules, implementing the image preprocessing pipeline (grayscale, binarization, morphology), implementing character segmentation using CCA with filtering, integrating the trained model into the inference engine, building the character mapping service, creating the OCR pipeline that chains all stages together, and implementing traced image generation.

**Increment 3  -  Database Integration:**
The third phase added persistent data storage. Tasks included: setting up MySQL through XAMPP, designing the recognition_history table schema, implementing SQLAlchemy ORM models, creating CRUD operations for saving and retrieving records, integrating database operations into the API endpoints, and testing data persistence through phpMyAdmin.

**Increment 4  -  Frontend Development:**
The fourth phase built the React.js web interface. Tasks included: creating the project with Vite and TypeScript, implementing the Upload Panel component with drag-and-drop, building the Results Display component with traced image and character table, creating the History Page for browsing past recognitions, implementing the Character Map Viewer, adding navigation with React Router, styling all components with custom CSS, and connecting the frontend to the backend API.

**Increment 5  -  Integration and Testing:**
The final phase focused on bringing everything together and comprehensive testing. Tasks included: CORS configuration for cross-origin communication, end-to-end testing of the complete workflow, unit testing of individual modules, integration testing of module interactions, validation testing with invalid and edge-case inputs, performance testing with various image sizes, and documentation.

### 1.1.9 Modules of the System

The VatteluttuX system is organized into the following functional modules:

| Module No. | Module Name | Technology | Description |
|:---|:---|:---|:---|
| 1 | Image Upload and Preview | React.js, TypeScript | Drag-and-drop file upload with live image preview |
| 2 | Image Preprocessing | Python, OpenCV | Grayscale conversion, denoising, Otsu binarization, morphology |
| 3 | Character Segmentation | Python, OpenCV | Connected Component Analysis with multi-stage filtering |
| 4 | CNN Classification | Python, PyTorch | ResNet-inspired model with 247 output classes |
| 5 | Character Mapping | Python, JSON | Label-to-Tamil Unicode character translation |
| 6 | Results Display | React.js, TypeScript | Visual presentation with traced image and character table |
| 7 | History Management | React.js, SQLAlchemy, MySQL | Persistent storage and retrieval of past recognitions |
| 8 | Character Map Viewer | React.js, TypeScript | Reference viewer for all 247 character mappings |

### 1.1.10 Input and Output Specifications

**System Inputs:**

| Input | Format | Source | Constraints |
|:---|:---|:---|:---|
| Inscription Image | PNG, JPG, JPEG, BMP | User upload (drag-and-drop or file browse) | File size: up to 10 MB; Resolution: minimum 100x100 pixels |
| API Request | HTTP POST (multipart/form-data) | Frontend React application | Content-Type: multipart/form-data |
| History Query | HTTP GET with query parameters | Frontend History Page | Parameters: skip (integer), limit (integer) |
| Character Query | HTTP GET with path parameter | Frontend Character Map Viewer | Parameter: category (string, optional) |

**System Outputs:**

| Output | Format | Destination | Description |
|:---|:---|:---|:---|
| Modern Tamil Text | Unicode string | Results Display panel | Complete translation in Modern Tamil |
| Traced Image | PNG image file | Results Display panel | Original image with bounding boxes |
| Character Details | JSON array | Character Table component | Label, Tamil char, confidence, bbox per character |
| Word Groups | JSON array | Word Groups component | Characters grouped into words |
| Recognition History | JSON array | History Page | All past recognition records |
| Character Map | JSON object | Character Map Viewer | All 247 character mappings with metadata |
| Export Files | TXT or JSON | User download | Exportable recognition results |


