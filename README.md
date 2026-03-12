# PDF to Markdown Converter

A versatile Python application that converts PDF files into clean, AI-ready Markdown format. Features both graphical and command-line interfaces, with optional OCR support for extracting text from images.

## 🌟 Features

- **Dual Interface**: Both GUI and command-line versions for different use cases
- **Smart Text Extraction**: Preserves document structure using HTML-to-Markdown conversion
- **OCR Support**: Optional text extraction from images using Tesseract-OCR
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Headless Operation**: CLI version works in server/container environments
- **Comprehensive Testing**: Built-in test suite for functionality verification
- **Automated Setup**: One-command installation and dependency management

## 📋 Requirements

### Minimum Requirements
- **Python 3.6+** (tested with Python 3.10)
- **pip** package manager

### Optional Dependencies
- **Tesseract-OCR** (for image text extraction)
- **Display server** (for GUI version only)

### Python Dependencies
All Python dependencies are automatically installed by the setup script:
- `customtkinter` - Modern GUI framework
- `PyMuPDF` - PDF processing library
- `markdownify` - HTML to Markdown conversion
- `pytesseract` - Tesseract OCR wrapper
- `Pillow` - Image processing

## 🚀 Installation

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/shinose/pdf2md.git
cd pdf2md

# Run automated setup
./setup.sh
```

The setup script will:
- Check Python version compatibility
- Install all required Python packages
- Verify Tesseract availability
- Test all components
- Report any issues

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shinose/pdf2md.git
   cd pdf2md
   ```

2. **Install Python dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Install Tesseract-OCR (Optional):**
   ```bash
   # Ubuntu/Debian
   sudo apt install tesseract-ocr
   
   # Fedora/CentOS/RHEL
   sudo dnf install tesseract
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

## 📖 Usage

### GUI Application

Launch the graphical interface for interactive use:

```bash
python3 pdf2md.py
```

**GUI Workflow:**
1. Click **"Select PDF"** to choose a PDF file
2. Click **"Convert to Markdown"** to process the document
3. Review the generated Markdown in the text area
4. Click **"Save Markdown"** to export the result

### Command-Line Interface

Perfect for automation, batch processing, or headless environments:

**Standard CLI:**
```bash
python3 pdf2md_cli.py <input_pdf> [-o output_file]
```

**Enhanced CLI (Recommended):**
```bash
python3 pdf2md_cli_enhanced.py <input_pdf> [options]
```

**Enhanced CLI Options:**
- `--no-ocr`: Disable OCR processing
- `--no-embed`: Don't embed images as base64
- `-o, --output`: Output Markdown file path

**CLI Examples:**
```bash
# Basic conversion with default settings
python3 pdf2md_cli_enhanced.py document.pdf

# Convert and save to file
python3 pdf2md_cli_enhanced.py document.pdf -o document.md

# Disable OCR for faster processing
python3 pdf2md_cli_enhanced.py document.pdf --no-ocr

# Don't embed images (smaller file size)
python3 pdf2md_cli_enhanced.py document.pdf --no-embed -o document.md

# Full processing with all features
python3 pdf2md_cli_enhanced.py document.pdf -o full_output.md

# Batch conversion (shell script)
for file in *.pdf; do
    python3 pdf2md_cli_enhanced.py "$file" -o "${file%.pdf}_enhanced.md"
done
```

### Testing and Verification

Run the comprehensive test suite:

```bash
python3 test_converter.py
```

This tests:
- Module imports
- PDF processing capabilities
- HTML-to-Markdown conversion
- GUI creation (in environments with display)
- Tesseract integration

### Creating Test Documents

Generate test PDFs for development or testing:

```bash
python3 create_test_pdf.py
```

Creates `test_document.pdf` with sample content for testing conversions.

## 🔧 Technical Details

### PDF Processing Pipeline

1. **Text Extraction**: Uses PyMuPDF to extract text as HTML (preserves structure)
2. **Image Processing**: Extracts embedded images and optionally applies OCR
3. **Markdown Conversion**: Converts HTML content to clean Markdown
4. **Output**: Displays or saves the final Markdown

### OCR Integration

- **Automatic Detection**: Checks for Tesseract availability
- **Graceful Degradation**: Works without OCR (images are skipped)
- **Error Handling**: Continues processing if individual images fail
- **Text Formatting**: OCR output is wrapped in `<pre>` tags for readability

### Error Handling

- **Missing Dependencies**: Clear error messages with installation instructions
- **Invalid Files**: Proper validation and user feedback
- **Processing Errors**: Graceful failure with detailed error information
- **OCR Failures**: Continues processing if individual images can't be processed

## 📁 Project Structure

```
pdf2md/
├── pdf2md.py              # Original GUI application
├── pdf2md_enhanced.py     # Enhanced GUI with better OCR and options
├── pdf2md_cli.py          # Standard command-line interface
├── pdf2md_cli_enhanced.py # Enhanced CLI with advanced features
├── setup.sh               # Automated setup script
├── install_tesseract.sh   # Tesseract installation helper
├── test_converter.py      # Test suite
├── create_test_pdf.py     # Test document generator
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history
└── LICENSE               # MIT License
```

## 🐛 Troubleshooting

### Common Issues

**GUI doesn't start:**
```bash
# Check if display is available
echo $DISPLAY

# Use CLI version instead
python3 pdf2md_cli.py document.pdf
```

**Tesseract not found:**
```bash
# Check if installed
which tesseract

# Run installation helper
./install_tesseract.sh

# Or install manually on Ubuntu/Debian
sudo apt install tesseract-ocr

# Verify installation
tesseract --version
```

**Module import errors:**
```bash
# Reinstall dependencies
python3 -m pip install -r requirements.txt --force-reinstall
```

**Permission errors:**
```bash
# Use user installation
python3 -m pip install --user -r requirements.txt
```

### Getting Help

1. Run the test suite: `python3 test_converter.py`
2. Check the setup script output: `./setup.sh`
3. Verify all dependencies are installed
4. Ensure PDF files are not password-protected

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/pdf2md.git
cd pdf2md

# Install dependencies
./setup.sh

# Run tests
python3 test_converter.py

# Create test PDFs
python3 create_test_pdf.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyMuPDF** - PDF processing library
- **CustomTkinter** - Modern GUI framework
- **Tesseract** - OCR engine
- **Markdownify** - HTML to Markdown conversion

## 📊 Version History

- **v1.0** - Initial release with GUI interface
- **v1.1** - Added CLI interface, setup script, and testing utilities
- **v1.2** - Enhanced documentation and error handling

---

**Made with ❤️ for the PDF-to-Markdown conversion community**
