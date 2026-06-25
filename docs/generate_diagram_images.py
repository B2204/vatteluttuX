
import base64
import urllib.request
import os
from pathlib import Path

def generate_mermaid_image(mermaid_code, output_path):
    # Encode mermaid code to base64
    graph_bytes = mermaid_code.encode('utf-8')
    base64_bytes = base64.b64encode(graph_bytes)
    base64_string = base64_bytes.decode('utf-8')
    
    # URL for mermaid.ink
    url = f"https://mermaid.ink/img/{base64_string}"
    
    try:
        print(f"Generating image for: {output_path.name}...")
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.read())
                print(f"Successfully saved to {output_path}")
            else:
                print(f"Failed to generate image. Status code: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

# Define diagrams
docs_dir = Path(r"f:\final mca project\VattalettuX\docs")
assets_dir = docs_dir / "assets"

# 1. Architectural Diagram
arch_code = """
graph TD
    classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1;
    classDef backend fill:#f1f8e9,stroke:#689f38,stroke-width:2px,color:#33691e;
    classDef pipe fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#e65100;
    classDef storage fill:#eceff1,stroke:#455a64,stroke-width:2px,color:#263238;

    User([User/Researcher]) <--> Frontend[React.js Web Interface]:::frontend
    Frontend <--> API[FastAPI Backend]:::backend
    
    subgraph Pipeline ["OCR Processing Pipeline"]
        API --> Preprocessor[Image Preprocessor]:::pipe
        Preprocessor --> Segmenter[Character Segmenter]:::pipe
        Segmenter --> Classifier[CNN Classification Engine]:::pipe
        Classifier --> Mapper[Character Mapping Service]:::pipe
    end
    
    subgraph Storage ["Storage & Resources"]
        Classifier -- Loads --> Weights[(Model Weights)]:::storage
        Mapper -- Queries --> CharMap[(Character Map)]:::storage
        API -- Data --> Media[(Media Storage)]:::storage
    end
    
    Mapper --> API
"""

# 2. Data Flow Diagram
dfd_code = """
graph LR
    classDef user fill:#f8f9fa,stroke:#343a40,stroke-width:2px,color:#212529;
    classDef input fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef ml_core fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#e65100;
    classDef mapping fill:#f1f8e9,stroke:#33691e,stroke-width:2px,color:#33691e;
    classDef result fill:#ede7f6,stroke:#512da8,stroke-width:2px,color:#311b92;
    classDef storage fill:#ffffff,stroke:#455a64,stroke-dasharray: 5 5,color:#455a64;

    U([User/Researcher]):::user -- "Upload Inscription" --> P1[Input Processing]:::input
    P1 -- "Cleaned Image" --> P2[Segmentation & Feature Extraction]:::input
    P2 -- "Character Chips" --> P3[Deep Learning Inference]:::ml_core
    
    subgraph KnowledgeBase ["Knowledge Base / Resources"]
        M[(Model Weights .pth)]:::storage --> P3
        K[(Mapping Data .json)]:::storage --> P4
    end
    
    P3 -- "Class Probabilities" --> P4[Character Translation]:::mapping
    P4 -- "Tamil Text Data" --> P5[Result Generation]:::result
    P5 -- "Annotated Outcome" --> U
"""

# 3. ER Diagram
erd_code = """
graph TD
    classDef tableHead fill:#263238,color:#ffffff,stroke:#263238,stroke-width:2px;
    classDef tableBody fill:#ffffff,stroke:#cfd8dc,stroke-width:1px;

    subgraph Schema ["Visual Database Schema"]
        T1_H[<b>INSCRIPTION_IMAGE</b>]:::tableHead
        T1_B["image_id (PK)<br/>file_path<br/>upload_date<br/>dimensions"]:::tableBody
        T1_H --- T1_B

        T2_H[<b>SEGMENTED_CHARACTER</b>]:::tableHead
        T2_B["char_id (PK)<br/>image_id (FK)<br/>bounding_box<br/>crop_path"]:::tableBody
        T2_H --- T2_B

        T3_H[<b>PREDICTION</b>]:::tableHead
        T3_B["prediction_id (PK)<br/>char_id (FK)<br/>label_id (FK)<br/>confidence"]:::tableBody
        T3_H --- T3_B

        T4_H[<b>CHARACTER_MAP</b>]:::tableHead
        T4_B["label_id (PK)<br/>modern_tamil<br/>unicode<br/>category"]:::tableBody
        T4_H --- T4_B

        T1_B -- "contains" --> T2_H
        T2_B -- "results in" --> T3_H
        T4_B -- "defines" --> T3_H
    end
"""

generate_mermaid_image(arch_code, assets_dir / "architecture.png")
generate_mermaid_image(dfd_code, assets_dir / "dfd.png")
generate_mermaid_image(erd_code, assets_dir / "erd.png")
print("Done.")
