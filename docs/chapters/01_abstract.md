# ABSTRACT

Vatteluttu is an ancient writing system that was widely used to write the Tamil language between the 3rd and 12th centuries CE. Thousands of stone inscriptions written in this script still exist across South India today, found on temple walls, rock surfaces, and copper plates. These inscriptions carry valuable information about the history, culture, governance, and daily life of ancient Tamil kingdoms such as the Cholas, Pandyas, and Pallavas. However, most of these inscriptions remain unread because only a very small number of trained experts — known as epigraphists — can understand this script. As a result, a huge amount of historical knowledge is simply not reaching the public.

This project presents **VattalettuX**, a web-based system that uses deep learning to automatically read Vatteluttu characters from photographs of stone inscriptions and convert them into their equivalent Modern Tamil text. The system works through a clearly defined four-step pipeline. First, the uploaded inscription image is cleaned and enhanced using image preprocessing techniques such as adaptive thresholding, morphological noise removal, and contrast enhancement. Second, individual characters are isolated from the cleaned image using Connected Component Analysis. Third, each segmented character is classified by a ResNet-inspired Convolutional Neural Network (CNN) trained to recognize 247 different Vatteluttu character forms — the most comprehensive character set used in any published Vatteluttu OCR study. Fourth, the recognized character codes are mapped to their corresponding Modern Tamil Unicode characters using a bidirectional mapping database.

The deep learning model was trained on a synthetically generated dataset of 247,000 images (1,000 variations per character class), created by applying realistic augmentations such as rotation, shearing, stroke variation, Gaussian noise, and textured stone-like backgrounds. The model achieved an overall Top-1 classification accuracy of 92.8% and a Top-5 accuracy of 98.1% on the held-out test set.

The complete system is deployed as a web application with a **React.js** frontend and a **Python FastAPI** backend. Users can upload inscription photographs through a drag-and-drop interface and receive the translated Modern Tamil text within seconds. The application also features a character mapping viewer, recognition history page backed by a **MySQL** database, and visual bounding box overlays showing each detected character. The average end-to-end processing time is approximately 1.8 seconds per image on a standard CPU.

VattalettuX demonstrates that modern deep learning techniques can be effectively applied to the challenging problem of ancient script recognition, even when working with a large number of visually similar character classes and degraded stone surfaces. The system serves as a practical tool for archaeologists, historians, and Tamil scholars, and as a foundation for future enhancements such as word-level recognition, transformer-based models, and mobile field applications.

&nbsp;

**Keywords:** Vatteluttu, Ancient Tamil Script, Optical Character Recognition, Convolutional Neural Network, Deep Learning, Image Processing, Epigraphy, ResNet, FastAPI, React.js, Character Segmentation, Modern Tamil Mapping.

---
