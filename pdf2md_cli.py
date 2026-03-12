#!/usr/bin/env python3
"""
Command-line version of PDF to Markdown Converter
"""

import sys
import os
import argparse
import fitz  # PyMuPDF
from markdownify import markdownify as md
import pytesseract
from PIL import Image
import io
import shutil

def convert_pdf_to_markdown(pdf_path, output_path=None):
    """
    Convert PDF to Markdown with optional OCR for images
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found")
        return False
    
    tesseract_installed = shutil.which("tesseract") is not None
    
    try:
        doc = fitz.open(pdf_path)
        content = ""
        images_found = False

        print(f"Processing {len(doc)} pages...")

        for i, page in enumerate(doc):
            print(f"Processing page {i + 1}...")
            
            # Extract text as HTML to preserve structure
            page_html = page.get_text("html")
            content += page_html
            
            # Extract images
            image_list = page.get_images(full=True)
            if image_list:
                images_found = True
                print(f"  Found {len(image_list)} images on page {i + 1}")

            if not tesseract_installed and images_found:
                print("  Skipping image processing (Tesseract not installed)")
                continue

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    # Perform OCR
                    ocr_text = pytesseract.image_to_string(image)
                    if ocr_text.strip():
                        content += f"\n\n<p>[Image content:]</p>\n<pre>{ocr_text}</pre>\n"
                        print(f"    Extracted text from image {img_index + 1}")
                except Exception as e:
                    print(f"    Could not process image {img_index + 1} on page {i + 1}: {e}")

        doc.close()

        if images_found and not tesseract_installed:
            print("\nWarning: Tesseract is not installed. Images were not converted to text.")
            print("To install Tesseract on Ubuntu/Debian: sudo apt install tesseract-ocr")

        # Convert to Markdown
        markdown_content = md(content)
        
        # Save or output
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"\n✓ Markdown saved to: {output_path}")
        else:
            print("\n" + "=" * 50)
            print("MARKDOWN OUTPUT:")
            print("=" * 50)
            print(markdown_content)
            print("=" * 50)
        
        return True

    except pytesseract.TesseractNotFoundError:
        print("Warning: Tesseract is not installed or not in your PATH. Images were not converted to text.")
        return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output Markdown file (optional)")
    
    args = parser.parse_args()
    
    print(f"Converting '{args.pdf_file}' to Markdown...")
    
    success = convert_pdf_to_markdown(args.pdf_file, args.output)
    
    if success:
        print("\n✓ Conversion completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
