import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from markdownify import markdownify as md
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import shutil
import base64
import os
import sys

def check_display_available():
    """Check if GUI display is available"""
    # Check for display environment variable
    if not os.environ.get('DISPLAY'):
        return False
    
    # Try to import and test tkinter
    try:
        test_tk = tk.Tk()
        test_tk.destroy()
        return True
    except:
        return False

def run_cli_fallback():
    """Fallback to CLI when GUI is not available"""
    print("🖥️  GUI not available - falling back to CLI mode")
    print("Use the enhanced CLI version instead:")
    print("python3 pdf2md_cli_enhanced.py <pdf_file> [options]")
    print("")
    print("Examples:")
    print("  python3 pdf2md_cli_enhanced.py document.pdf")
    print("  python3 pdf2md_cli_enhanced.py document.pdf -o output.md")
    print("  python3 pdf2md_cli_enhanced.py --help")
    print("")
    print("For GUI mode, ensure you're running in a desktop environment with X11 display.")

class EnhancedPDF2MarkdownConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Enhanced PDF to Markdown Converter")
        self.geometry("900x700")

        # Set theme
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # File selection
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.select_button = ctk.CTkButton(self.file_frame, text="Select PDF", command=self.select_pdf)
        self.select_button.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = ctk.CTkLabel(self.file_frame, text="No file selected", anchor="w")
        self.file_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Options frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure(2, weight=1)

        # OCR option
        self.ocr_var = tk.BooleanVar(value=True)
        self.ocr_checkbox = ctk.CTkCheckBox(self.options_frame, text="Enable OCR (if available)", variable=self.ocr_var)
        self.ocr_checkbox.grid(row=0, column=0, padx=10, pady=5)

        # Embed images option
        self.embed_var = tk.BooleanVar(value=True)
        self.embed_checkbox = ctk.CTkCheckBox(self.options_frame, text="Embed images as base64", variable=self.embed_var)
        self.embed_checkbox.grid(row=0, column=1, padx=10, pady=5)

        # Status label
        self.status_label = ctk.CTkLabel(self.options_frame, text="Ready", anchor="e")
        self.status_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        # Conversion button
        self.convert_button = ctk.CTkButton(self, text="Convert to Markdown", command=self.convert_pdf)
        self.convert_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Markdown display
        self.textbox = ctk.CTkTextbox(self, wrap=tk.WORD)
        self.textbox.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Save button
        self.save_button = ctk.CTkButton(self, text="Save Markdown", command=self.save_markdown)
        self.save_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        
        self.pdf_path = None
        self.tesseract_installed = shutil.which("tesseract") is not None

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if self.pdf_path:
            self.file_label.configure(text=self.pdf_path)
            self.textbox.delete("1.0", tk.END)
            self.update_status(f"Selected: {self.pdf_path.split('/')[-1]}")

    def update_status(self, message):
        self.status_label.configure(text=message)
        self.update_idletasks()

    def preprocess_image(self, image):
        """Enhance image for better OCR accuracy"""
        try:
            # Convert to grayscale if needed
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
        except Exception as e:
            print(f"Image preprocessing failed: {e}")
            return image

    def extract_text_with_ocr(self, image, page_num, img_index):
        """Extract text with enhanced OCR processing"""
        if not self.tesseract_installed or not self.ocr_var.get():
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
            print(f"OCR failed for image {img_index} on page {page_num}: {e}")
        
        return None

    def image_to_base64(self, image_bytes):
        """Convert image to base64 for embedding"""
        try:
            return base64.b64encode(image_bytes).decode('utf-8')
        except:
            return None

    def convert_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        self.update_status("Converting...")
        self.convert_button.configure(state="disabled")
        
        try:
            doc = fitz.open(self.pdf_path)
            content = ""
            total_pages = len(doc)
            images_processed = 0
            ocr_results = []

            for i, page in enumerate(doc):
                self.update_status(f"Processing page {i+1}/{total_pages}")
                
                # Extract text as HTML to preserve structure
                page_html = page.get_text("html")
                content += page_html
                
                # Extract images
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Try OCR if enabled and available
                    ocr_result = None
                    if self.ocr_var.get() and self.tesseract_installed:
                        try:
                            image = Image.open(io.BytesIO(image_bytes))
                            ocr_result = self.extract_text_with_ocr(image, i+1, img_index+1)
                            if ocr_result:
                                ocr_results.append(ocr_result)
                                content += f"\n\n<!-- Image {img_index+1} on page {i+1} - OCR Confidence: {ocr_result['confidence']:.1f}% -->\n"
                                content += f"<div class='image-content'>\n<pre>{ocr_result['text']}</pre>\n</div>\n"
                                images_processed += 1
                        except Exception as e:
                            print(f"Could not process image {img_index} on page {i+1}: {e}")
                    
                    # Embed image if option is enabled
                    if self.embed_var.get():
                        img_b64 = self.image_to_base64(image_bytes)
                        if img_b64:
                            img_format = base_image["ext"]
                            content += f"\n\n![Image {img_index+1} on page {i+1}](data:image/{img_format};base64,{img_b64[:100]}...)\n"

            doc.close()

            # Add summary
            if ocr_results:
                avg_confidence = sum(r['confidence'] for r in ocr_results) / len(ocr_results)
                content = f"<!-- OCR Summary: {len(ocr_results)} images processed, avg confidence: {avg_confidence:.1f}% -->\n\n" + content

            # Convert to Markdown
            markdown_content = md(content)
            
            # Add processing summary at the top
            summary = f"# PDF Conversion Summary\n\n"
            summary += f"- **Total Pages:** {total_pages}\n"
            summary += f"- **Images Found:** {sum(len(page.get_images(full=True)) for page in doc) if doc else 0}\n"
            summary += f"- **OCR Processed:** {len(ocr_results)}\n"
            summary += f"- **OCR Available:** {'Yes' if self.tesseract_installed else 'No'}\n"
            summary += f"- **Images Embedded:** {'Yes' if self.embed_var.get() else 'No'}\n\n"
            
            if not self.tesseract_installed:
                summary += "⚠️ **Note:** Tesseract OCR is not installed. Install it for image text extraction:\n"
                summary += "```bash\nsudo apt install tesseract-ocr\n```\n\n"
            
            summary += "---\n\n"
            
            final_content = summary + markdown_content
            
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, final_content)
            
            self.update_status(f"Complete! {len(ocr_results)} images processed with OCR")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")
            self.update_status("Error")
        finally:
            self.convert_button.configure(state="normal")

    def save_markdown(self):
        markdown_content = self.textbox.get("1.0", tk.END)
        if not markdown_content.strip():
            messagebox.showerror("Error", "No content to save.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Markdown file",
            defaultextension=".md",
            filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
        )

        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                messagebox.showinfo("Success", f"Markdown file saved to {save_path}")
                self.update_status(f"Saved: {save_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving: {e}")

if __name__ == "__main__":
    # Check if GUI display is available
    if not check_display_available():
        run_cli_fallback()
        sys.exit(1)
    
    # Run GUI if display is available
    app = EnhancedPDF2MarkdownConverter()
    app.mainloop()
