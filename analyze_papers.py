import os
import sys
from pypdf import PdfReader

# Force UTF-8 for stdout just in case, though we will primarily write to file
sys.stdout.reconfigure(encoding='utf-8')

def extract_text_from_pdf(pdf_path, output_file):
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        # Extract text from the first 5 pages and last 2 pages
        pages_to_extract = list(range(min(5, num_pages)))
        if num_pages > 5:
            pages_to_extract.extend(range(max(5, num_pages - 2), num_pages))
            
        header = f"\n\n{'='*20}\nAnalyzing {os.path.basename(pdf_path)} ({num_pages} pages)\n{'='*20}\n"
        output_file.write(header)
        print(f"Analyzing {os.path.basename(pdf_path)}...")
        
        for i in sorted(list(set(pages_to_extract))):
            page = reader.pages[i]
            page_text = page.extract_text()
            page_header = f"\n--- Page {i+1} ---\n"
            output_file.write(page_header)
            output_file.write(page_text)
            
    except Exception as e:
        error_msg = f"Error reading {pdf_path}: {e}\n"
        print(error_msg)
        output_file.write(error_msg)

def main():
    paper_dir = os.path.join(os.getcwd(), 'PAPER')
    output_path = os.path.join(os.getcwd(), 'paper_content.txt')
    
    if not os.path.exists(paper_dir):
        print(f"Directory not found: {paper_dir}")
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        for filename in os.listdir(paper_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(paper_dir, filename)
                extract_text_from_pdf(pdf_path, f)
    
    print(f"Analysis complete. Output saved to {output_path}")

if __name__ == "__main__":
    main()
