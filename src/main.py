import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
import time

def select_pdf():
    """Open file dialog to select PDF file"""
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        entry_pdf_path.delete(0, tk.END)
        entry_pdf_path.insert(0, pdf_path)

def select_output_folder():
    """Open directory dialog to select output folder"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(0, folder_path)

def log_message(message):
    """Append message to log text area"""
    log_text.insert(tk.END, message + '\n')
    log_text.see(tk.END)
    root.update_idletasks()

def convert_pdf():
    """Convert PDF to images with progress tracking"""
    pdf_path = entry_pdf_path.get()
    output_folder = entry_output_folder.get()

    if not pdf_path or not output_folder:
        messagebox.showerror("Error", "Please select a PDF file and output folder")
        return

    try:
        log_message("Starting conversion...")
        start_time = time.time()
        
        # Convert PDF to list of images
        pages = convert_from_path(pdf_path, dpi=300)
        total_pages = len(pages)
        log_message(f"Found {total_pages} pages in PDF")

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Convert each page to image
        for i, page in enumerate(pages):
            page_number = str(i + 1).zfill(3)  # Formato a 3 cifre (001, 002, ...)
            image_path = os.path.join(output_folder, f"page_{page_number}.png")
            page.save(image_path, "PNG")
            log_message(f"Converted page {page_number}/{total_pages}")
            
            # Update progress bar
            progress_var.set((i + 1) / total_pages * 100)
            root.update_idletasks()

        # Show completion message
        elapsed_time = time.time() - start_time
        log_message(f"Conversion completed in {elapsed_time:.2f} seconds")
        messagebox.showinfo("Success", 
            f"Converted {total_pages} pages in {elapsed_time:.2f} seconds")

    except Exception as e:
        log_message(f"Error: {str(e)}")
        messagebox.showerror("Conversion Error", str(e))
    finally:
        progress_var.set(0)

# Create main window
root = tk.Tk()
root.title("PDF to Image Converter")
root.geometry("600x500")
root.resizable(False, False)

# PDF selection section
tk.Label(root, text="PDF File:").pack(pady=5)
entry_pdf_path = tk.Entry(root, width=70)
entry_pdf_path.pack(padx=10)
tk.Button(root, text="Browse PDF", command=select_pdf).pack(pady=5)

# Output folder selection
tk.Label(root, text="Output Folder:").pack(pady=5)
entry_output_folder = tk.Entry(root, width=70)
entry_output_folder.pack(padx=10)
tk.Button(root, text="Browse Folder", command=select_output_folder).pack(pady=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill='x', padx=20)

# Log text area
log_frame = tk.Frame(root)
log_frame.pack(pady=10, padx=10, fill='both', expand=True)
tk.Label(log_frame, text="Conversion Log:").pack(anchor='w')
log_text = tk.Text(log_frame, height=10)
log_text.pack(fill='both', expand=True)

# Conversion button
convert_btn = tk.Button(root, text="Convert to Images", 
                        command=convert_pdf, bg='#4CAF50', fg='white')
convert_btn.pack(pady=10)

# Start GUI
root.mainloop()

