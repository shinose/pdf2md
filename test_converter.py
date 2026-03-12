#!/usr/bin/env python3
"""
Test script to verify PDF2MarkdownConverter functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf2md import PDF2MarkdownConverter
import fitz  # PyMuPDF
from markdownify import markdownify as md

def test_pdf_processing():
    """Test the core PDF processing functionality"""
    print("Testing PDF processing components...")
    
    # Test 1: Check if all modules can be imported
    try:
        import customtkinter as ctk
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import fitz
        from markdownify import markdownify as md
        import pytesseract
        from PIL import Image
        import io
        import shutil
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 2: Check Tesseract availability
    tesseract_installed = shutil.which("tesseract") is not None
    if tesseract_installed:
        print("✓ Tesseract is available")
    else:
        print("⚠ Tesseract is not installed (OCR functionality will be limited)")
    
    # Test 3: Test basic HTML to Markdown conversion
    try:
        html_content = "<h1>Test Header</h1><p>Test paragraph</p>"
        markdown_content = md(html_content)
        print(f"✓ HTML to Markdown conversion works: {markdown_content}")
    except Exception as e:
        print(f"✗ HTML to Markdown conversion failed: {e}")
        return False
    
    # Test 4: Test PyMuPDF functionality
    try:
        # Create a simple test PDF in memory
        doc = fitz.open()  # Create empty PDF
        page = doc.new_page()
        page.insert_text((72, 72), "Test PDF content")
        
        # Test text extraction
        text = page.get_text()
        print(f"✓ PDF text extraction works: '{text.strip()}'")
        
        # Test HTML extraction
        html = page.get_text("html")
        print(f"✓ PDF HTML extraction works: {len(html)} characters")
        
        doc.close()
    except Exception as e:
        print(f"✗ PDF processing failed: {e}")
        return False
    
    print("\n✓ All core functionality tests passed!")
    return True

def test_gui_creation():
    """Test GUI creation (without showing the window)"""
    print("\nTesting GUI creation...")
    
    try:
        # Create the app instance but don't show it
        app = PDF2MarkdownConverter()
        print("✓ GUI application created successfully")
        
        # Test that all widgets exist
        if hasattr(app, 'select_button') and hasattr(app, 'convert_button'):
            print("✓ GUI widgets are properly initialized")
        
        # Clean up
        app.destroy()
        print("✓ GUI cleanup successful")
        return True
        
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False

if __name__ == "__main__":
    print("PDF to Markdown Converter - Test Suite")
    print("=" * 50)
    
    # Run tests
    pdf_test_passed = test_pdf_processing()
    gui_test_passed = test_gui_creation()
    
    print("\n" + "=" * 50)
    if pdf_test_passed and gui_test_passed:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python3 pdf2md.py")
        print("\nNote: Without Tesseract, image OCR will not work.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
