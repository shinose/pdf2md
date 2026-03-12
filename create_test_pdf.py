#!/usr/bin/env python3
"""
Create a simple test PDF for testing the converter
"""

import fitz  # PyMuPDF

def create_test_pdf():
    """Create a simple test PDF with text"""
    doc = fitz.open()  # Create empty PDF
    
    # Add first page
    page = doc.new_page()
    page.insert_text((72, 72), "Test PDF Document")
    page.insert_text((72, 100), "This is a test PDF created for testing the PDF to Markdown converter.")
    page.insert_text((72, 130), "It contains some sample text to verify the conversion works correctly.")
    
    # Add second page
    page = doc.new_page()
    page.insert_text((72, 72), "Page 2")
    page.insert_text((72, 100), "This is the second page of the test PDF.")
    page.insert_text((72, 130), "The converter should handle multiple pages correctly.")
    
    # Save the PDF
    doc.save("test_document.pdf")
    doc.close()
    
    print("✓ Test PDF 'test_document.pdf' created successfully")

if __name__ == "__main__":
    create_test_pdf()
