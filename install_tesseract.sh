#!/bin/bash

# Tesseract Installation Helper Script
# This script helps install Tesseract OCR for different systems

echo "Tesseract OCR Installation Helper"
echo "================================="

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        echo "Detected Debian/Ubuntu system"
        echo "To install Tesseract, run:"
        echo "sudo apt update"
        echo "sudo apt install tesseract-ocr"
        echo ""
        echo "For additional language packs:"
        echo "sudo apt install tesseract-ocr-eng"
        
    elif command -v dnf &> /dev/null; then
        # Fedora/CentOS/RHEL
        echo "Detected Fedora/CentOS/RHEL system"
        echo "To install Tesseract, run:"
        echo "sudo dnf install tesseract"
        
    elif command -v yum &> /dev/null; then
        # Older CentOS/RHEL
        echo "Detected older CentOS/RHEL system"
        echo "To install Tesseract, run:"
        echo "sudo yum install tesseract"
        
    else
        echo "Unknown Linux distribution"
        echo "Please check your package manager for Tesseract OCR"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS system"
    if command -v brew &> /dev/null; then
        echo "To install Tesseract with Homebrew:"
        echo "brew install tesseract"
        echo "brew install tesseract-lang"  # For additional languages
    else
        echo "Homebrew not found. Install Homebrew first:"
        echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "Then run: brew install tesseract"
    fi
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "Detected Windows system"
    echo "Download Tesseract installer from:"
    echo "https://github.com/UB-Mannheim/tesseract/wiki"
    echo ""
    echo "After installation, add Tesseract to your PATH:"
    echo "C:\\Program Files\\Tesseract-OCR"
    
else
    echo "Unknown operating system: $OSTYPE"
    echo "Please install Tesseract OCR manually"
fi

echo ""
echo "After installation, verify it works:"
echo "tesseract --version"
echo ""
echo "Then test the enhanced converter:"
echo "python3 pdf2md_cli_enhanced.py your_document.pdf"
