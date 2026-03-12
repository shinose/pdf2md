# PDF to Markdown Converter

A simple, cross-platform desktop application to convert PDF files into AI-ready Markdown, including text from images using Optical Character Recognition (OCR).

## Features

*   **PDF to Markdown:** Converts the text content of a PDF file into clean Markdown.
*   **OCR for Images:** Extracts text from images within the PDF using Tesseract-OCR.
*   **Simple GUI:** An intuitive graphical user interface built with `customtkinter`.
*   **Cross-Platform:** Works on Linux and Windows.

## Requirements

Before you begin, ensure you have met the following requirements:

*   **Python 3:** You have a recent version of Python 3 installed.
*   **Tesseract-OCR:** You have Tesseract-OCR installed on your system.

### Tesseract Installation

Tesseract is an open-source OCR engine. You must install it for the image-to-text functionality to work.

*   **On Fedora/CentOS/RHEL:**
    ```bash
    sudo dnf install tesseract
    ```
*   **On Debian/Ubuntu:**
    ```bash
    sudo apt install tesseract-ocr
    ```
*   **On Windows:**
    Download and run the installer from the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page. Make sure to add the Tesseract installation directory to your system's `PATH`.

## Installation

### Quick Setup (Recommended)

Run the setup script to automatically install dependencies and verify everything works:

```bash
./setup.sh
```

### Manual Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If you are using git
    git clone <repository_url>
    cd pdf2md
    ```

2.  **Install Python dependencies:**
    The required Python libraries are listed in `requirements.txt`. Install them using `pip`:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

3.  **Install Tesseract-OCR (Optional but recommended):**
    See the Tesseract installation section below.

## Usage

### GUI Application

To run the graphical user interface:

```bash
python3 pdf2md.py
```

This will launch the "PDF to Markdown Converter" window.

1.  Click **"Select PDF"** to choose a PDF file.
2.  Click **"Convert to Markdown"**. The application will process the PDF, including running OCR on any images.
3.  The generated Markdown will appear in the text box.
4.  Click **"Save Markdown"** to save the result to a `.md` file.

### Command-Line Interface

For headless environments or automation:

```bash
python3 pdf2md_cli.py <pdf_file> [-o output.md]
```

**Examples:**
```bash
# Convert and display output in terminal
python3 pdf2md_cli.py document.pdf

# Convert and save to file
python3 pdf2md_cli.py document.pdf -o document.md

# Convert with custom output path
python3 pdf2md_cli.py "/path/to/document.pdf" -o "/path/to/output.md"
```

### Testing

A test script is included to verify functionality:

```bash
python3 test_converter.py
```

This will test all components and report any issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
