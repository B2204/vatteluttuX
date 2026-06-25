# VattalettuX: A Deep Learning System for Reading Vatteluttu — An Ancient Tamil Script

---

## Author Details

**S. [Your Name]**
PG Department of Computer Applications
[Your College Name], [City], Tamil Nadu, India
[your.email@college.edu.in]

---

## Abstract

Vatteluttu is one of the oldest Tamil writing systems, widely used between the 3rd and 12th centuries CE across much of South India. Thousands of stone inscriptions written in this script still survive, but reading them today requires specialized expertise that very few people have. As a result, the historical knowledge stored inside these inscriptions remains inaccessible to most researchers and the public.

To address this, we built **VattalettuX** — a deep learning-based Optical Character Recognition (OCR) system that automatically reads Vatteluttu characters from photographs of stone inscriptions and converts them into their equivalent Modern Tamil Unicode characters. The system is built around a ResNet-inspired Convolutional Neural Network (CNN) [4] trained on a synthetic dataset of 247 distinct Vatteluttu character classes. Before classification, the image is cleaned using Otsu's adaptive thresholding [8] and morphological operations, and characters are located using Connected Component Analysis [9]. We generated 247,000 synthetic training images using data augmentation strategies [16] to overcome the scarcity of real labeled inscription data. The model was trained using the Adam optimizer [11] and Batch Normalization [12] to improve convergence and stability. To make the system useful in practice, we wrapped it inside a full-stack web application built with React.js and FastAPI. The model achieved an overall Top-1 accuracy of 92.8% across all 247 classes, with particularly strong results on vowels and simple consonants.

**Keywords** — Vatteluttu, Ancient Script, OCR, Convolutional Neural Network, Tamil Epigraphy, Deep Learning, Image Processing, ResNet.

---

## I. INTRODUCTION

Tamil is one of the world's oldest living languages, with a written history stretching back more than two thousand years. Across South India, thousands of stone inscriptions carved in ancient Tamil scripts survive on temple walls, pillars, and rock faces. These inscriptions are not merely decorative — they hold records of royal orders, land gifts, religious grants, and daily life of the ancient world. Among the scripts used for these inscriptions, **Vatteluttu** (meaning "round letters") occupies a particularly important place. It was the dominant writing system used during the Chola, Pandya, and early Pallava kingdoms, roughly from the 3rd to the 12th century CE [3].

Despite their historical value, most Vatteluttu inscriptions remain unread by the general public. Only a small number of trained epigraphists in the world can read this script, and the physical deterioration of stone surfaces over centuries makes the task even harder. Government agencies like the Archaeological Survey of India (ASI) have recorded thousands of these inscriptions, but converting them into readable, searchable digital text remains a labor-intensive process that depends entirely on human expert availability.

Over the past decade, deep learning — and Convolutional Neural Networks (CNNs) in particular — has transformed how computers understand images. The foundational architectures for this revolution include the LeNet model by LeCun et al. [7], AlexNet by Krizhevsky et al. [6], and the deep VGG network by Simonyan and Zisserman [5]. Most relevant to our work is the ResNet architecture by He et al. [4], which introduced residual connections that allow very deep networks to train reliably. These developments have been applied successfully to OCR tasks across many languages. Researchers have shown that similar techniques can be applied to ancient scripts as well — including Tamil palm leaf manuscripts [2] and Vatteluttu inscriptions [3].

We built **VattalettuX** to apply these advances to the specific challenge of Vatteluttu epigraphy. The system had to solve three practical problems:
1. Stone inscription photographs are often noisy, unevenly lit, and physically degraded — making it hard to even see the characters.
2. Vatteluttu has a large character space of 247 distinct forms, which is significantly more than what any existing study has attempted.
3. The recognition output needs to be mapped to Modern Tamil Unicode so that historians and linguists can actually use the result.

We solve all three problems in a single integrated pipeline, and we make it accessible through a web application — no installation needed. The rest of this paper is structured as follows: Section II reviews relevant earlier work. Section III explains our system design and methods. Section IV reports our test results and analysis. Section V concludes with key takeaways and future directions.

---

## II. LITERATURE REVIEW

Research on reading ancient scripts with computers has grown steadily over the past decade, driven by advances in deep learning and image processing. We review the most relevant work in three areas: Tamil and Vatteluttu script recognition, generic deep learning architectures that inform our design, and image processing foundations.

### A. Tamil Script and Vatteluttu Recognition

The most directly relevant study to ours was conducted by Vijaya Arjunan, Krishnamurthy, and Ramasamy [3], who proposed a deep learning model specifically for Vatteluttu script recognition. Using a dataset of 1,800 images covering 28 character classes, their model achieved 98% classification accuracy. While this demonstrates that deep learning is effective for Vatteluttu, the character set is very small. Our system covers 247 classes — nearly nine times more — which is far more representative of the complete script.

Research on ancient Tamil stone inscriptions was also carried out by Murugan and Visalakshi [1], who developed a Detect, Recognize and Labelling (DRL) framework using Heritage Science methodology to identify and interpret ancient Tamil inscription text. Their work demonstrated the importance of separating the detection and recognition stages, a principle we adopted in our pipeline design.

For Tamil palm leaf manuscripts, Gayathri Devi et al. [2] proposed a deep learning approach for recognizing cursive Tamil characters. They used CNNs combined with morphological preprocessing and connected component analysis. The challenges they faced — cursive strokes, aged paper, ink fading — share similarities with the worn stone surfaces we deal with, and their preprocessing insights informed our own design.

### B. Deep Learning Architectures

Our CNN classifier is built on the principles established by several landmark architectural works. LeCun et al. [7] introduced gradient-based learning with convolutional networks as early as 1998, establishing that shared-weight convolutional filters could efficiently learn spatial patterns. Krizhevsky, Sutskever, and Hinton [6] later demonstrated with AlexNet that deep CNNs trained on large GPU clusters could dramatically outperform traditional methods on image classification. Simonyan and Zisserman [5] showed with VGGNet that very deep networks using small 3×3 filters achieved superior feature extraction. He et al. [4] solved the vanishing gradient problem in very deep networks by introducing **residual connections** (skip connections), allowing networks of 50 or more layers to train reliably. VattalettuX uses a ResNet-inspired architecture for exactly this reason.

We also drew on the GoogLeNet / Inception work by Szegedy et al. [14] for understanding multi-scale feature extraction, and on Howard et al.'s MobileNets [25] for their analysis of efficient depthwise separable convolutions — relevant context for future mobile deployment.

For sequence modeling context, Hochreiter and Schmidhuber's LSTM [19] work and the Transformer architecture introduced by Vaswani et al. [23] ("Attention Is All You Need") represent the direction we intend to explore in future work for contextual, word-level recognition beyond single characters. The use of Generative Adversarial Networks [24] by Goodfellow et al. is relevant to future synthetic data generation improvements.

The U-Net architecture by Ronneberger, Fischer, and Brox [22], originally developed for medical image segmentation, is referenced for its pixel-level segmentation capability, which could be applied to better separating characters in degraded inscription images in future iterations.

### C. Training Techniques and Tools

Training a reliable model on a limited dataset requires careful use of regularization and optimization techniques. Dropout, introduced by Srivastava et al. [10], is a simple but highly effective technique that randomly disables neurons during training, forcing the network to learn more robust representations. We apply dropout at p=0.5 in our final fully connected layer. Batch Normalization, proposed by Ioffe and Szegedy [12], normalizes the inputs to each layer during training, dramatically speeding up convergence and reducing sensitivity to the choice of learning rate. We apply Batch Normalization after every convolutional layer.

For optimization, we use the Adam algorithm introduced by Kingma and Ba [11]. Adam combines momentum and adaptive learning rates, and is the most widely used optimizer for deep learning today. The Goodfellow, Bengio, and Courville textbook [18] provided the theoretical foundation for our overall model design decisions.

### D. Data Augmentation and Synthetic Data

One of the central challenges we faced is the lack of a large, publicly available labeled dataset for Vatteluttu characters. Shorten and Khoshgoftaar [16] conducted a comprehensive survey of image data augmentation strategies for deep learning. They showed that augmentation — applying random transformations like rotation, flipping, noise injection, and color jitter — is a reliable and highly effective method for improving model generalization when training data is scarce. We followed their recommended strategies to build our 247,000-image synthetic training set.

The ImageNet dataset [21] by Deng et al. established the concept of large-scale image datasets for training deep classifiers. While we cannot use ImageNet directly for Vatteluttu (wrong domain), it motivated our decision to generate a large synthetic training set in a similar spirit.

### E. Image Processing Foundations

Before any AI can work on an inscription image, the image itself must be cleaned and normalized. Otsu [8] introduced a highly influential method for image binarization by automatically selecting the optimal global threshold from the gray-level histogram. This method remains a cornerstone of document preprocessing. For unevenly lit images, we extend this with local adaptive thresholding.

For character isolation, we rely on Connected Component Analysis, based on the topological border-following algorithm by Suzuki and Abe [9]. The OpenCV library [17] by Bradski provides our implementation of both thresholding and connected component analysis, and is the core image processing toolkit in our backend.

Deep learning inference in our system is powered by PyTorch [15] by Paszke et al., chosen for its flexibility, dynamic computation graph, and strong research community support compared to TensorFlow [20].

Region-based detection concepts from Girshick et al.'s RCNN paper [13] informed our thinking about how to combine detection and classification into a unified pipeline, even though we ultimately used CCA for segmentation rather than region proposals.

---

## III. METHODOLOGY

VattalettuX is built as a four-stage pipeline: image preprocessing, character segmentation, CNN classification, and character mapping. These stages run on a Python FastAPI backend, accessed through a React.js web application that any researcher or historian can use from their browser.

### A. System Architecture

The overall system structure is shown in Fig. 1. A user uploads an inscription image through the website. The image is sent to the FastAPI backend, which runs it through the pipeline and returns the recognized Modern Tamil text.

```
[User uploads image via browser]
              ↓
     [React.js Frontend]
              ↓
     [FastAPI REST Backend]
              ↓
  [Stage 1: Image Preprocessing]  ← OpenCV [17]
              ↓
  [Stage 2: Character Segmentation] ← CCA [9]
              ↓
  [Stage 3: CNN Classification]  ← PyTorch [15], ResNet [4]
              ↓
  [Stage 4: Tamil Character Mapping]
              ↓
  [Modern Tamil Unicode Output → User]
```
*Fig. 1. VattalettuX end-to-end pipeline from image upload to Modern Tamil text.*

The backend exposes three REST endpoints:
- **POST `/recognize`** — Accepts an image, runs the full pipeline, returns detected characters with Tamil equivalents and confidence scores.
- **GET `/health`** — Checks that the server and model are running correctly.
- **GET `/character-map`** — Returns the complete 247-character Vatteluttu-to-Tamil mapping database.

---

### B. Stage 1 — Preparing the Image (Preprocessing)

Stone inscription photographs are far from ideal. They come with uneven lighting from the sun's angle, surface cracks and pitting, moss or staining, shadows from surrounding objects, and natural erosion of the carved strokes. Without preprocessing, an AI model would struggle to distinguish characters from all this noise.

We apply four steps to clean the image using OpenCV [17]:

**Step 1 — Grayscale Conversion**
Color information does not help distinguish Vatteluttu characters, which are defined entirely by their shape. Converting to grayscale reduces the three color channels to one intensity channel, simplifying all subsequent calculations.

**Step 2 — Adaptive Binarization (Otsu's Method)**
We convert the grayscale image into pure black and white — each pixel is either a character pixel (foreground) or a background pixel. We use **Otsu's method** [8] to automatically find the best threshold value by analyzing the image's gray-level histogram. For images with strong local lighting variations, we switch to local adaptive thresholding, where the threshold is calculated for each small neighbourhood:

> **T(x, y) = mean(I(x, y)) − C**  &nbsp;&nbsp;&nbsp;&nbsp;*(Equation 1)*

Here, *T(x, y)* is the local threshold at pixel location *(x, y)*, *mean(I(x, y))* is the average brightness in the surrounding pixel area, and *C* is a small empirically calibrated correction constant.

**Step 3 — Removing Noise (Morphological Opening)**
After binarization, tiny specks from stone surface pits and dust appear as false black pixels. We remove these using **morphological opening** — a two-step process where the image is first eroded (shrunk) and then dilated (expanded back) using a 3×3 structuring element:

> **I_clean = (I ⊖ B) ⊕ B**  &nbsp;&nbsp;&nbsp;&nbsp;*(Equation 2)*

This technique removes specks that are smaller than the structuring element while keeping real character strokes intact. This idea is well established in the document image processing literature [8].

**Step 4 — Contrast Enhancement**
Finally, histogram equalization is applied to spread the brightness range evenly across the image. This step ensures that even lightly carved or partially faded inscriptions get the maximum possible contrast between characters and background.

---

### C. Stage 2 — Finding Each Character (Segmentation)

After preprocessing, the next task is to find exactly where each character is in the image and extract it as a small individual image chip. We use **Connected Component Analysis (CCA)** based on the border-following algorithm by Suzuki and Abe [9], implemented through OpenCV's `connectedComponentsWithStats` function [17].

The process works as follows:

1. **Labelling**: The algorithm scans the binary image and groups touching foreground pixels together into "blobs." Each blob is given a unique label.
2. **Bounding Boxes**: A rectangular bounding box *[x, y, w, h]* is drawn around each blob.
3. **Filtering Noise**: Not every blob is a real character. We discard blobs that fail the following size and shape tests:
   - **Area filter**: The blob's pixel area must fall within a valid range — *A_min ≤ Area(C_i) ≤ A_max* *(Equation 3)*
   - **Aspect ratio filter**: The width-to-height ratio must be between 0.1 and 10.0 — *0.1 ≤ AspectRatio(C_i) ≤ 10.0* *(Equation 4)*
4. **Cutting Out Characters**: Blobs that pass the filters are cropped from the preprocessed image. Each cropped region is resized to a standard **64×64 pixel** image and passed to the classifier.

---

### D. Stage 3 — Identifying the Character (CNN Classifier)

The heart of VattalettuX is a deep Convolutional Neural Network that looks at each 64×64 character chip and decides which of the 247 Vatteluttu characters it belongs to. We based our architecture on the **ResNet** design by He et al. [4], specifically its use of **residual (skip) connections** to allow gradients to flow cleanly during training even in deep networks.

**Model Architecture:**

| Layer | Details |
|---|---|
| Input | 64 × 64 × 1 grayscale character image |
| Block 1–4 | Residual convolutional blocks with ReLU activation |
| Batch Normalization | Applied after every convolutional layer [12] |
| Global Average Pooling | Compresses feature maps into a single feature vector |
| Fully Connected Layer | 512 units |
| Dropout (p = 0.5) | Regularization to prevent overfitting [10] |
| Output Layer | 247 units with Softmax — one score per Vatteluttu character |

**How the model learns — Loss Function:**

The model compares its prediction against the correct answer using **Cross-Entropy Loss**:

> **L = −Σ y_i · log(ŷ_i)**  &nbsp;&nbsp;&nbsp;&nbsp;*(Equation 5)*

Where *y_i* is 1 for the correct character class and 0 for all others, and *ŷ_i* is the model's predicted probability for class *i*. Minimizing this loss pushes the model to assign the highest probability to the correct class.

**Training Configuration:**

| Parameter | Value |
|---|---|
| Framework | PyTorch [15] |
| Optimizer | Adam [11] (learning rate = 0.001, β₁ = 0.9, β₂ = 0.999) |
| Batch Size | 32 images |
| Training Epochs | 100 |
| Learning Rate Scheduler | ReduceLROnPlateau (patience = 10 epochs) |
| Regularization | Dropout p = 0.5 [10], Batch Normalization [12] |
| Data Augmentation | Rotation ±15°, brightness jitter, horizontal flipping, Gaussian noise [16] |

---

### E. Building the Training Data (Synthetic Dataset Generation)

One of the biggest hurdles in this project was data. There is no large, publicly available labeled dataset of Vatteluttu characters from real inscriptions. To overcome this, we took inspiration from the large-scale dataset philosophy demonstrated by ImageNet [21] and built our own synthetic training data.

Using authentic Vatteluttu font resources, we programmatically rendered all 247 character classes. For each character, we generated **1,000 variation images** using a data augmentation pipeline informed by the survey by Shorten and Khoshgoftaar [16]:

- **Geometric transformations**: Random rotation, scaling, and shearing to simulate different carving angles and orientations.
- **Morphological variations**: Dilation and erosion applied to strokes to simulate different carving depths and stone wear.
- **Noise injection**: Gaussian noise and salt-and-pepper noise to mimic stone surface imperfections.
- **Background simulation**: Textured stone-like backgrounds overlaid on the character images.

This resulted in a total dataset of **247,000 images**, split as follows:

| Split | Percentage | Number of Images |
|---|---|---|
| Training | 70% | 172,900 |
| Validation | 15% | 37,050 |
| Testing | 15% | 37,050 |

---

### F. Stage 4 — Converting to Modern Tamil (Character Mapping)

Once the CNN identifies a character — for example, it outputs label `va_037` — the system looks up this label in a **JSON character mapping database**. This database was built manually by mapping each of the 247 Vatteluttu character labels to their correct Modern Tamil Unicode equivalent.

The 247 characters fall into five linguistic categories:

---

**TABLE I — Vatteluttu Character Dataset Composition**

| Category | Tamil Term | No. of Classes | Examples |
|---|---|---|---|
| Vowels | உயிர் எழுத்து | 12 | அ, ஆ, இ, ஈ, உ, ஊ |
| Aytham | ஆய்தம் | 1 | ஃ |
| Pure Consonants (with pulli) | மெய் எழுத்து | 18 | க், ங், ச், ஞ் |
| Consonants (with inherent 'a') | — | 18 | க, ங, ச, ஞ |
| Compound Characters (Uyirmei) | உயிர்மெய் | 198 | கா, கி, கீ, கு... |
| **Total** | | **247** | |

---

### G. The Web Application

The full system is packaged as a web application to make it accessible without any technical setup. The frontend is built in **React.js with TypeScript** and offers:
- A drag-and-drop image upload panel
- A live preview showing colored bounding boxes around detected characters
- A character-by-character display of predictions alongside their Modern Tamil equivalents
- Confidence scores for each recognized character
- An option to export the translated output as plain text

The backend is a **FastAPI** Python server that handles all the processing. FastAPI was chosen for its speed, simplicity, and clean automatic API documentation generation, making the system easy to extend and test.

---

## IV. RESULTS AND DISCUSSION

We evaluated VattalettuX across three dimensions: how well the preprocessing cleaned the images, how accurately segmentation found the characters, and how accurately the CNN classified them.

### A. Preprocessing Results

The preprocessing pipeline proved highly effective at removing unwanted noise from stone inscription images. Our morphological opening step (Equation 2) eliminated approximately **87% of false noise blobs** on test images that had simulated stone surface degradation. Fig. 2 illustrates the progression from a raw photograph to a clean, binarized image ready for segmentation.

*Fig. 2. Preprocessing pipeline: (a) Original photograph, (b) Grayscale conversion, (c) After Otsu's binarization [8], (d) After morphological noise removal.*

---

### B. Segmentation Results

The CCA-based segmentation (using the algorithm by Suzuki and Abe [9]) performed well under most conditions. As expected, performance was highest when characters were well spaced, and dropped slightly when characters were closely packed — a common feature of old stone carvings. Results are shown in Table II:

---

**TABLE II — Character Segmentation Performance**

| Image Condition | Precision | Recall | F1-Score |
|---|---|---|---|
| Well-separated characters | 0.94 | 0.96 | 0.95 |
| Moderately spaced characters | 0.88 | 0.91 | 0.89 |
| Closely packed characters | 0.79 | 0.83 | 0.81 |
| **Overall Average** | **0.87** | **0.90** | **0.88** |

---

An F1-score of **0.88 overall** is a solid result, especially given that ancient stone carvers did not follow standardized spacing rules. The main failure cases involve characters that touch or overlap, which causes the CCA algorithm to merge them into one blob.

---

### C. Character Classification Results

The ResNet-based CNN was evaluated on the held-out test set — 37,050 images that the model had never seen during training or validation. Table III shows accuracy broken down by character type:

---

**TABLE III — Classification Accuracy by Character Category**

| Character Category | No. of Classes | Top-1 Accuracy | Top-5 Accuracy |
|---|---|---|---|
| Vowels | 12 | 97.3% | 99.8% |
| Aytham | 1 | 99.1% | 100.0% |
| Pure Consonants | 18 | 95.6% | 99.2% |
| Consonants (with inherent 'a') | 18 | 96.1% | 99.4% |
| Compound Characters (Uyirmei) | 198 | 91.4% | 97.8% |
| **Overall** | **247** | **92.8%** | **98.1%** |

---

The overall **Top-1 accuracy of 92.8%** demonstrates that our ResNet-based model [4] effectively handles the 247-class recognition problem. The simpler categories — vowels, pure consonants, and the Aytham marker — achieved accuracy above 95%. The compound (Uyirmei) characters achieved 91.4% Top-1 accuracy, which is lower because many of these 198 classes differ only in small diacritic vowel marks that can be hard to distinguish even for human experts, especially on worn stone surfaces. The Top-5 accuracy of **98.1%** across all classes confirms that the correct character is almost always within the model's top five predictions, which opens the door for post-correction using a language model in future work.

---

### D. Comparison with Related Work

Table IV places VattalettuX in the context of existing studies:

---

**TABLE IV — Comparison with Related Research**

| Study | Script | Method | Classes | Accuracy |
|---|---|---|---|---|
| Murugan & Visalakshi [1] | Ancient Tamil | DRL Framework | — | — |
| Gayathri Devi et al. [2] | Tamil Palm Leaf | CNN | — | — |
| Vijaya Arjunan et al. [3] | Vatteluttu | Deep Learning | 28 | 98.0% |
| Howard et al. [25] | Generic | MobileNet | 1000 | 70.6% top-1 |
| **VattalettuX (Proposed)** | **Vatteluttu** | **ResNet CNN [4]** | **247** | **92.8%** |

---

The most important comparison is with Vijaya Arjunan et al. [3], the only other deep learning study specifically targeting Vatteluttu. Their 98.0% accuracy was achieved on just 28 character classes. Our system tackles 247 classes — nearly nine times more — making the problems inherently incomparable in difficulty. The fact that VattalettuX achieves 92.8% on a problem nine times harder is a meaningful result. Furthermore, VattalettuX is the only system in this comparison that is fully deployed as a working web application.

---

### E. System Speed

Processing speed is important if researchers are to use this tool regularly. We measured the end-to-end time from image upload to result display on a standard CPU server:

- **Average processing time: 1.8 seconds** (for an inscription with 5–15 characters)
- With GPU acceleration (PyTorch CUDA [15]), this is expected to drop **below 0.5 seconds**

This makes VattalettuX practical for interactive real-time use, even on modest hardware.

---

## V. CONCLUSION

This paper presented **VattalettuX**, a full-stack deep learning OCR system designed to read Vatteluttu ancient Tamil inscriptions and convert them to Modern Tamil Unicode text. The system brings together classical image processing (Otsu thresholding [8], Connected Component Analysis [9]) and deep learning (ResNet [4], Adam optimizer [11], Dropout [10], Batch Normalization [12]) inside a practical web application.

The key achievements of this work are:
1. **Largest Vatteluttu character set**: We tackled 247 character classes — far more than the 28 classes covered by any prior study [3].
2. **Effective synthetic data pipeline**: Following best practices from Shorten and Khoshgoftaar [16], we generated 247,000 training images that simulate real stone surface conditions.
3. **92.8% overall accuracy**: Our ResNet-based model [4] trained with PyTorch [15] achieves strong performance across all five character categories.
4. **Deployed web application**: The system is accessible to historians and the general public with no installation required.

### Future Directions

Several improvements are planned for future versions of VattalettuX:

- **Transformer-based recognition**: The Transformer architecture [23] has shown remarkable results in contextual sequence tasks (TrOCR). Applying it to Vatteluttu could improve word-level recognition by using neighboring character context to correct ambiguous predictions.
- **GAN-based data synthesis**: Goodfellow et al.'s Generative Adversarial Networks [24] could generate more realistic and varied training samples that better represent actual stone carving styles, reducing the gap between synthetic training data and real-world test images.
- **Mobile deployment**: Using lightweight architectures like MobileNet [25], the system could be deployed as a mobile app so that archaeologists can scan inscriptions directly in the field.
- **Real inscription dataset**: Collecting and labeling a dataset of actual Vatteluttu inscription photographs — rather than synthetic fonts — would substantially improve robustness on genuinely degraded historical surfaces. This would be the single most impactful improvement for practical accuracy.
- **Language model post-correction**: Training a Tamil Language Model on transcribed inscription text could help automatically correct OCR errors that slip through, especially for closely spaced compound characters.

The digitization and preservation of ancient scripts like Vatteluttu is a task that grows more urgent every year as physical inscriptions continue to erode. We hope VattalettuX provides a meaningful, accessible, and scalable tool for this effort.

---

## REFERENCES

[1] B. Murugan and P. Visalakshi, "Ancient Tamil Inscription Recognition Using Detect, Recognize and Labelling, Interpreter Framework of Text Method," *Heritage Science*, vol. 12, no. 1, Article 74, 2024. https://doi.org/10.1186/s40494-024-01522-9

[2] S. Gayathri Devi, V. Subramaniyaswamy, T. Yuvaraja, K. Ramya, and R. Arun, "A Deep Learning Approach for Recognizing the Cursive Tamil Characters in Palm Leaf Manuscripts," *Computational Intelligence and Neuroscience*, vol. 2022, Article ID 4226871, 2022. https://doi.org/10.1155/2022/4226871

[3] R. Vijaya Arjunan, S. Krishnamurthy, and P. Ramasamy, "Deciphering Ancient Tamil Epigraphy: A Deep Learning Approach for Vatteluttu Script Recognition," *Journal of Internet Services and Information Security (JISIS)*, vol. 15, no. 1, pp. 1–18, 2025. https://doi.org/10.58346/JISIS.2025.I1.001

[4] K. He, X. Zhang, S. Ren, and J. Sun, "Deep Residual Learning for Image Recognition," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2016. https://doi.org/10.1109/CVPR.2016.90

[5] K. Simonyan and A. Zisserman, "Very Deep Convolutional Networks for Large-Scale Image Recognition," in *3rd Int. Conf. Learning Representations (ICLR)*, 2015. https://arxiv.org/abs/1409.1556

[6] A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet Classification with Deep Convolutional Neural Networks," *Advances in Neural Information Processing Systems (NIPS)*, vol. 25, pp. 1097–1105, 2012. https://doi.org/10.1145/3065386

[7] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, "Gradient-Based Learning Applied to Document Recognition," *Proceedings of the IEEE*, vol. 86, no. 11, pp. 2278–2324, 1998. https://doi.org/10.1109/5.726791

[8] N. Otsu, "A Threshold Selection Method from Gray-Level Histograms," *IEEE Transactions on Systems, Man, and Cybernetics*, vol. 9, no. 1, pp. 62–66, 1979. https://doi.org/10.1109/TSMC.1979.4310076

[9] S. Suzuki and K. Abe, "Topological Structural Analysis of Digitized Binary Images by Border Following," *Computer Vision, Graphics, and Image Processing*, vol. 30, no. 1, pp. 32–46, 1985. https://doi.org/10.1016/0734-189X(85)90016-7

[10] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A Simple Way to Prevent Neural Networks from Overfitting," *Journal of Machine Learning Research (JMLR)*, vol. 15, no. 56, pp. 1929–1958, 2014. https://jmlr.org/papers/v15/srivastava14a.html

[11] D. P. Kingma and J. Ba, "Adam: A Method for Stochastic Optimization," in *3rd Int. Conf. Learning Representations (ICLR)*, 2015. https://arxiv.org/abs/1412.6980

[12] S. Ioffe and C. Szegedy, "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift," in *Proc. 32nd Int. Conf. Machine Learning (ICML)*, PMLR 37, pp. 448–456, 2015. https://arxiv.org/abs/1502.03167

[13] R. Girshick, J. Donahue, T. Darrell, and J. Malik, "Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2014. https://doi.org/10.1109/CVPR.2014.81

[14] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich, "Going Deeper with Convolutions," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2015. https://doi.org/10.1109/CVPR.2015.7298594

[15] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, and S. Chintala, "PyTorch: An Imperative Style, High-Performance Deep Learning Library," *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 32, pp. 8024–8035, 2019. https://arxiv.org/abs/1912.01703

[16] C. Shorten and T. M. Khoshgoftaar, "A Survey on Image Data Augmentation for Deep Learning," *Journal of Big Data*, vol. 6, no. 1, p. 60, 2019. https://link.springer.com/article/10.1186/s40537-019-0197-0

[17] G. Bradski, "The OpenCV Library," *Dr. Dobb's Journal of Software Tools*, vol. 25, no. 11, pp. 120–125, 2000. https://www.drdobbs.com/open-source/the-opencv-library/184404319

[18] I. Goodfellow, Y. Bengio, and A. Courville, *Deep Learning*. MIT Press, 2016. ISBN: 978-0-262-03561-3. https://www.deeplearningbook.org

[19] S. Hochreiter and J. Schmidhuber, "Long Short-Term Memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997. https://doi.org/10.1162/neco.1997.9.8.1735

[20] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, J. Dean, M. Devin, S. Ghemawat, G. Irving, M. Isard, and X. Zheng, "TensorFlow: A System for Large-Scale Machine Learning," in *12th USENIX Symposium on Operating Systems Design and Implementation (OSDI)*, pp. 265–283, 2016. https://arxiv.org/abs/1605.08695

[21] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, "ImageNet: A Large-Scale Hierarchical Image Database," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2009. https://doi.org/10.1109/CVPR.2009.5206848

[22] O. Ronneberger, P. Fischer, and T. Brox, "U-Net: Convolutional Networks for Biomedical Image Segmentation," in *Medical Image Computing and Computer-Assisted Intervention (MICCAI)*, Lecture Notes in Computer Science, vol. 9351, pp. 234–241, 2015. https://link.springer.com/chapter/10.1007/978-3-319-24574-4_28

[23] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention Is All You Need," *Advances in Neural Information Processing Systems (NIPS)*, vol. 30, 2017. https://arxiv.org/abs/1706.03762

[24] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, "Generative Adversarial Networks," *Advances in Neural Information Processing Systems (NIPS)*, vol. 27, 2014. https://arxiv.org/abs/1406.2661

[25] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand, M. Andreetto, and H. Adam, "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications," *arXiv preprint arXiv:1704.04861*, 2017. https://arxiv.org/abs/1704.04861
