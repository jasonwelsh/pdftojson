#!/usr/bin/env python3
import pdfplumber
import json
from typing import List, Dict
import re
import sys

def extract_pdf_data(pdf_path: str) -> List[Dict]:
    structured_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            paragraphs = text.split('\n\n')
            for para_num, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    data_point = {
                        'page_number': page_num + 1,
                        'paragraph_number': para_num + 1,
                        'content': paragraph.strip(),
                        'word_count': len(paragraph.split()),
                        'metadata': {
                            'has_numbers': bool(re.search(r'\d', paragraph)),
                            'has_special_chars': bool(re.search(r'[^a-zA-Z0-9\s]', paragraph))
                        }
                    }
                    structured_data.append(data_point)
    return structured_data

def save_to_json(data: List[Dict], output_path: str) -> None:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) != 3:
        print("Usage: pdftojson <pdf_file> <json_output_file>")
        print("Example: pdftojson input.pdf output.json")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    json_output_path = sys.argv[2]
    
    try:
        print(f"Processing PDF: {pdf_path}")
        extracted_data = extract_pdf_data(pdf_path)
        save_to_json(extracted_data, json_output_path)
        print(f"Successfully saved JSON data to: {json_output_path}")
        print(f"\nSummary:")
        print(f"Total paragraphs extracted: {len(extracted_data)}")
        print(f"Total pages processed: {extracted_data[-1]['page_number']}")
        
    except FileNotFoundError:
        print(f"Error: The PDF file '{pdf_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()