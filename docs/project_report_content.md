# VatteluttuX - Project Documentation

## Abstract
Ancient inscriptions are vital for understanding historical context, but reading scripts like Vatteluttu requires expert knowledge. **VatteluttuX** is an automated Optical Character Recognition (OCR) system designed to bridge this gap. Using a deep Convolutional Neural Network (CNN) trained on synthetic data, the system converts Vatteluttu inscriptions into modern Tamil Unicode text. The solution features a React-based web interface for easy uploading and visualization, coupled with a Python FastAPI backend that handles image preprocessing, segmentation, and classification. Initial results demonstrate the feasibility of preserving and digitizing ancient Tamil heritage through modern AI techniques.

## Problem Statement
Deciphering Vatteluttu inscriptions is currently a manual, time-consuming process restricted to a small circle of epigraphists. There is no publicly available, user-friendly tool to digitize these inscriptions. The goal is to build an end-to-end automated system that can take an image of a Vatteluttu script and output readable modern Tamil text, serving both academic researchers and the general public.

## Proposed System
VatteluttuX is a full-stack OCR solution:
1. **Frontend**: A responsive React application allowing users to upload images, view traced character detections, and export results.
2. **Backend**: A FastAPI server orchestrating the OCR pipeline.
3. **Core Engine**:
   - **Preprocessing**: Adaptive thresholding and noise removal using OpenCV.
   - **Segmentation**: Connected Component Analysis (CCA) to isolate characters.
   - **Classification**: A calibrated ResNet-based CNN model trained on 247 character classes (vowels, consonants, and combinations).
   - **Mapping**: A precise linguistic mapping layer converting predicted labels to Unicode Tamil.

## Character Dataset
VatteluttuX utilizes a comprehensive dataset of **247 Tamil characters**, each uniquely mapped from ancient Vatteluttu script to Modern Tamil Unicode. The dataset is organized into distinct categories:

### Dataset Structure
- **Vowels (உயிர் எழுத்துக்கள்)**: 12 characters (அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ)
- **Aytham (ஆய்தம்)**: 1 character (ஃ)
- **Pure Consonants (மெய் எழுத்துக்கள்)**: 18 characters with pulli (க், ங், ச், ஞ், etc.)
- **Consonants with inherent 'a'**: 18 characters (க, ங, ச, ஞ, etc.)
- **Uyirmei (உயிர்மெய் எழுத்துக்கள்)**: 198 combinations (consonant + vowel marks)

### Label Mapping System
Each character is assigned a unique label in the format `va_XXX` (e.g., `va_001` for அ, `va_023` for ம், `va_149` for மா). This systematic approach ensures:
- **Consistency**: Uniform identification across training and inference
- **Traceability**: Direct mapping between model outputs and Tamil Unicode
- **Scalability**: Easy extension for additional character variants

The complete character mappings can be accessed via:
- **API Endpoint**: `/character-map` - Returns full dataset with categories and statistics
- **Web Interface**: Character Mappings tab provides an interactive viewer with search and filtering capabilities

## System Architecture
The system follows a microservices-inspired architecture:
- **Client Layer**: React SPA (Single Page Application) interacting via REST API.
- **Service Layer**: Python FastAPI providing `/recognize` and `/health` endpoints.
- **Processing Layer**: PyTorch for inference and OpenCV for image manipulation.
- **Data Layer**: JSON-based persistent mapping for the 247-character Vatteluttu charset.

## Limitations & Future Work
**Limitations**:
- Currently optimized for clean, high-contrast images; degraded stone inscriptions may require enhanced preprocessing.
- Segmentation assumes relatively separated characters; touching characters (ligatures) may pose challenges.

**Future Work**:
- Transition to Transformer-based models (TrOCR) for better context awareness.
- Integration of a Language Model (LLM) to correct post-OCR text based on Tamil grammar.
- Mobile application development for on-site field usage by archaeologists.
