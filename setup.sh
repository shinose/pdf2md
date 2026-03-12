#!/bin/bash

# PDF to Markdown Converter Setup Script

echo "PDF to Markdown Converter Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "Python version: $python_version"

# Simple version comparison (works for 3.x versions)
if [[ $python_version == 3.* ]]; then
    echo "✓ Python version is compatible"
else
    echo "✗ Python 3.6+ is required"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed successfully"
else
    echo "✗ Failed to install Python dependencies"
    exit 1
fi

# Check Tesseract
echo ""
echo "Checking Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    echo "✓ Tesseract is installed"
    tesseract_version=$(tesseract --version 2>&1 | head -n1)
    echo "  Version: $tesseract_version"
else
    echo "⚠ Tesseract is not installed"
    echo "  To install on Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo "  To install on Fedora/CentOS: sudo dnf install tesseract"
    echo "  The application will work without Tesseract, but image OCR will be disabled."
fi

# Test imports
echo ""
echo "Testing Python imports..."
python3 -c "
import sys
modules = ['customtkinter', 'fitz', 'markdownify', 'pytesseract', 'PIL']
failed = []
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        print(f'✗ {module}')
        failed.append(module)

if failed:
    print(f'Failed modules: {failed}')
    sys.exit(1)
else:
    print('All modules imported successfully')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "To run the GUI application:"
    echo "  python3 pdf2md.py"
    echo ""
    echo "To run the command-line version:"
    echo "  python3 pdf2md_cli.py <pdf_file> [-o output.md]"
    echo ""
    echo "Example:"
    echo "  python3 pdf2md_cli.py document.pdf -o document.md"
else
    echo ""
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi
