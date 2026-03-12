#!/usr/bin/env python3
"""
Enhanced Command-line version of PDF to Markdown Converter
"""

import sys
import os
import argparse
import fitz  # PyMuPDF
from markdownify import markdownify as md
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import shutil
import base64

class EnhancedOCRProcessor:
    """Enhanced OCR processor with better image handling"""
    
    def __init__(self):
        self.tesseract_installed = shutil.which("tesseract") is not None
    
    def preprocess_image(self, image):
        """Enhance image for better OCR accuracy"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            # Apply median filter to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
        except Exception as e:
            print(f"    Image preprocessing failed: {e}")
            return image
    
    def extract_text_with_ocr(self, image, page_num, img_index):
        """Extract text with confidence scoring"""
        if not self.tesseract_installed:
            return None
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Get OCR data with confidence
            data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)
            
            # Extract text and calculate confidence
            text_parts = []
            confidences = []
            
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 0:
                    text_parts.append(data['text'][i])
                    confidences.append(data['conf'][i])
            
            text = ' '.join(text_parts).strip()
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            if text.strip() and avg_confidence > 30:  # Filter low-confidence results
                return {
                    'text': text,
                    'confidence': avg_confidence,
                    'page': page_num,
                    'image_index': img_index
                }
            
        except Exception as e:
            print(f"    OCR failed for image {img_index} on page {page_num}: {e}")
        
        return None
    
    def image_to_base64(self, image_bytes):
        """Convert image to base64 for embedding"""
        try:
            return base64.b64encode(image_bytes).decode('utf-8')
        except:
            return None

def convert_pdf_to_markdown(pdf_path, output_path=None, enable_ocr=True, embed_images=True):
    """
    Enhanced PDF to Markdown conversion with better OCR and image handling
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found")
        return False
    
    ocr_processor = EnhancedOCRProcessor()
    
    try:
        doc = fitz.open(pdf_path)
        content = ""
        total_pages = len(doc)
        images_processed = 0
        ocr_results = []
        total_images = 0

        print(f"Processing {total_pages} pages...")

        for i, page in enumerate(doc):
            print(f"Processing page {i + 1}/{total_pages}...")
            
            # Extract text as HTML to preserve structure
            page_html = page.get_text("html")
            content += page_html
            
            # Extract images
            image_list = page.get_images(full=True)
            total_images += len(image_list)
            
            if image_list:
                print(f"  Found {len(image_list)} images on page {i + 1}")

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Try OCR if enabled and available
                ocr_result = None
                if enable_ocr and ocr_processor.tesseract_installed:
                    try:
                        image = Image.open(io.BytesIO(image_bytes))
                        ocr_result = ocr_processor.extract_text_with_ocr(image, i+1, img_index+1)
                        if ocr_result:
                            ocr_results.append(ocr_result)
                            content += f"\n\n<!-- Image {img_index+1} on page {i+1} - OCR Confidence: {ocr_result['confidence']:.1f}% -->\n"
                            content += f"<div class='image-content'>\n<pre>{ocr_result['text']}</pre>\n</div>\n"
                            images_processed += 1
                            print(f"    Extracted text from image {img_index + 1} (confidence: {ocr_result['confidence']:.1f}%)")
                    except Exception as e:
                        print(f"    Could not process image {img_index + 1} on page {i + 1}: {e}")
                
                # Embed image if option is enabled
                if embed_images:
                    img_b64 = ocr_processor.image_to_base64(image_bytes)
                    if img_b64:
                        img_format = base_image["ext"]
                        # Truncate base64 for readability
                        content += f"\n\n![Image {img_index+1} on page {i+1}](data:image/{img_format};base64,{img_b64[:50]}...)\n"

        doc.close()

        # Add processing summary
        if ocr_results:
            avg_confidence = sum(r['confidence'] for r in ocr_results) / len(ocr_results)
            content = f"<!-- OCR Summary: {len(ocr_results)} images processed, avg confidence: {avg_confidence:.1f}% -->\n\n" + content
        
        # Convert to Markdown
        markdown_content = md(content)
        
        # Add processing summary at the top
        summary = f"# PDF Conversion Summary\n\n"
        summary += f"- **Source File:** `{os.path.basename(pdf_path)}`\n"
        summary += f"- **Total Pages:** {total_pages}\n"
        summary += f"- **Images Found:** {total_images}\n"
        summary += f"- **OCR Processed:** {len(ocr_results)}\n"
        summary += f"- **OCR Available:** {'Yes' if ocr_processor.tesseract_installed else 'No'}\n"
        summary += f"- **Images Embedded:** {'Yes' if embed_images else 'No'}\n\n"
        
        if not ocr_processor.tesseract_installed and enable_ocr:
            summary += "⚠️ **Note:** Tesseract OCR is not installed. Install it for image text extraction:\n"
            summary += "```bash\nsudo apt install tesseract-ocr\n```\n\n"
        
        if ocr_results:
            avg_confidence = sum(r['confidence'] for r in ocr_results) / len(ocr_results)
            summary += f"📊 **OCR Performance:** {len(ocr_results)} images processed with {avg_confidence:.1f}% average confidence\n\n"
        
        summary += "---\n\n"
        
        final_content = summary + markdown_content
        
        # Save or output
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print(f"\n✓ Markdown saved to: {output_path}")
        else:
            print("\n" + "=" * 50)
            print("MARKDOWN OUTPUT:")
            print("=" * 50)
            print(final_content)
            print("=" * 50)
        
        return True

    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced PDF to Markdown Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf                           # Convert with default settings
  %(prog)s document.pdf -o output.md              # Convert and save to file
  %(prog)s document.pdf --no-ocr                   # Disable OCR processing
  %(prog)s document.pdf --no-embed                # Don't embed images
  %(prog)s document.pdf --ocr --embed -o out.md    # Enable all features
        """
    )
    
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output Markdown file (optional)")
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR processing")
    parser.add_argument("--no-embed", action="store_true", help="Don't embed images as base64")
    
    args = parser.parse_args()
    
    enable_ocr = not args.no_ocr
    embed_images = not args.no_embed
    
    print(f"Converting '{args.pdf_file}' to Markdown...")
    print(f"OCR: {'Enabled' if enable_ocr else 'Disabled'}")
    print(f"Image Embedding: {'Enabled' if embed_images else 'Disabled'}")
    
    success = convert_pdf_to_markdown(args.pdf_file, args.output, enable_ocr, embed_images)
    
    if success:
        print("\n✓ Conversion completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
