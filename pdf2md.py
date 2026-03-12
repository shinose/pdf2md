import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from markdownify import markdownify as md
import pytesseract
from PIL import Image
import io
import shutil
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
    print("Use the CLI version instead:")
    print("python3 pdf2md_cli.py <pdf_file> [-o output.md]")
    print("")
    print("Or use the enhanced CLI:")
    print("python3 pdf2md_cli_enhanced.py <pdf_file> [options]")
    print("")
    print("Examples:")
    print("  python3 pdf2md_cli.py document.pdf")
    print("  python3 pdf2md_cli_enhanced.py document.pdf -o output.md")
    print("  python3 pdf2md_cli_enhanced.py --help")
    print("")
    print("For GUI mode, ensure you're running in a desktop environment with X11 display.")

class PDF2MarkdownConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF to Markdown Converter")
        self.geometry("800x600")

        # Set theme
        ctk.set_appearance_mode("System")  # System, Dark, Light
        ctk.set_default_color_theme("blue")  # blue, green, dark-blue

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # File selection
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.select_button = ctk.CTkButton(self.file_frame, text="Select PDF", command=self.select_pdf)
        self.select_button.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = ctk.CTkLabel(self.file_frame, text="No file selected", anchor="w")
        self.file_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Conversion button
        self.convert_button = ctk.CTkButton(self, text="Convert to Markdown", command=self.convert_pdf)
        self.convert_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Markdown display
        self.textbox = ctk.CTkTextbox(self, wrap=tk.WORD)
        self.textbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Save button
        self.save_button = ctk.CTkButton(self, text="Save Markdown", command=self.save_markdown)
        self.save_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        self.pdf_path = None

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if self.pdf_path:
            self.file_label.configure(text=self.pdf_path)
            self.textbox.delete("1.0", tk.END)

    def convert_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        tesseract_installed = shutil.which("tesseract") is not None
        
        try:
            doc = fitz.open(self.pdf_path)
            content = ""
            images_found = False

            for i, page in enumerate(doc):
                # Extract text as HTML to preserve structure
                content += page.get_text("html")
                
                # Extract images
                image_list = page.get_images(full=True)
                if image_list:
                    images_found = True

                if not tesseract_installed and images_found:
                    continue # Skip image processing if tesseract is not there

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
                    except Exception as e:
                        print(f"Could not process image {img_index} on page {i}: {e}")

            doc.close()

            if images_found and not tesseract_installed:
                messagebox.showwarning("Warning", "Tesseract is not installed or not in your PATH. Images were not converted to text.")

            markdown_content = md(content)
            
            self.textbox.delete("1.0", tk.END)
            self.textbox.insert(tk.END, markdown_content)

        except pytesseract.TesseractNotFoundError:
             messagebox.showwarning("Warning", "Tesseract is not installed or not in your PATH. Images were not converted to text.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")

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
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving: {e}")

if __name__ == "__main__":
    # Check if GUI display is available
    if not check_display_available():
        run_cli_fallback()
        sys.exit(1)
    
    # Run GUI if display is available
    app = PDF2MarkdownConverter()
    app.mainloop()
