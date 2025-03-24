import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
from pdf2image.pdf2image import pdfinfo_from_path
import time
from threading import Thread
import gc
import platform

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Image Converter Pro")
        self.root.geometry("700x600")
        self.setup_ui()
        self.conversion_in_corso = False
        self.should_stop = False
        
    def setup_ui(self):
        style = ttk.Style()
        style.configure('TButton', padding=6)
        style.configure('TFrame', background='#f0f0f0')
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # PDF selection
        pdf_frame = ttk.LabelFrame(main_frame, text="PDF File")
        pdf_frame.pack(fill='x', pady=5)
        
        self.entry_pdf_path = ttk.Entry(pdf_frame, width=60)
        self.entry_pdf_path.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(pdf_frame, text="Browse", command=self.select_pdf, width=10).pack(side='right', padx=5)
        
        # Output folder
        output_frame = ttk.LabelFrame(main_frame, text="Output Folder")
        output_frame.pack(fill='x', pady=5)
        
        self.entry_output_folder = ttk.Entry(output_frame, width=60)
        self.entry_output_folder.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(output_frame, text="Browse", command=self.select_output_folder, width=10).pack(side='right', padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options")
        options_frame.pack(fill='x', pady=5)
        
        ttk.Label(options_frame, text="DPI:").pack(side='left', padx=5)
        self.dpi_var = tk.IntVar(value=200)
        ttk.Spinbox(options_frame, from_=72, to=600, increment=50, textvariable=self.dpi_var, width=5).pack(side='left')
        
        ttk.Label(options_frame, text="Format:").pack(side='left', padx=(10,5))
        self.format_var = tk.StringVar(value='PNG')
        ttk.Combobox(options_frame, textvariable=self.format_var, values=['PNG', 'JPEG', 'TIFF'], width=6).pack(side='left')
        
        # Page range
        ttk.Label(options_frame, text="Pages:").pack(side='left', padx=(10,5))
        self.page_range_var = tk.StringVar(value='all')
        ttk.Entry(options_frame, textvariable=self.page_range_var, width=10).pack(side='left')
        ttk.Label(options_frame, text="(e.g. 1-5,8,10-12)").pack(side='left', padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=10)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log")
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=5)
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_conversion, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        self.convert_btn = ttk.Button(button_frame, text="Convert", command=self.start_conversion)
        self.convert_btn.pack(side='right', padx=5)
    
    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            self.entry_pdf_path.delete(0, tk.END)
            self.entry_pdf_path.insert(0, pdf_path)
    
    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_output_folder.delete(0, tk.END)
            self.entry_output_folder.insert(0, folder_path)
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def stop_conversion(self):
        self.should_stop = True
        self.log_message("Conversion stopping after current page...")
    
    def start_conversion(self):
        if self.conversion_in_corso:
            return
            
        self.conversion_in_corso = True
        self.should_stop = False
        self.convert_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        Thread(target=self.convert_pdf, daemon=True).start()
    
    def parse_page_range(self, page_range_str, max_pages):
        if not page_range_str or page_range_str.lower() == 'all':
            return list(range(1, max_pages + 1))
        
        pages = set()
        parts = page_range_str.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        
        return sorted(p for p in pages if 1 <= p <= max_pages)
    
    def convert_pdf(self):
        try:
            pdf_path = self.entry_pdf_path.get()
            output_folder = self.entry_output_folder.get()
            dpi = self.dpi_var.get()
            fmt = self.format_var.get().lower()
            page_range = self.page_range_var.get()

            if not pdf_path or not output_folder:
                messagebox.showerror("Error", "Please select a PDF file and output folder")
                return

            self.log_message(f"Starting conversion at {dpi} DPI to {fmt.upper()}...")
            start_time = time.time()
            
            # Get PDF info
            info = pdfinfo_from_path(pdf_path)
            total_pages = info["Pages"]
            self.log_message(f"Found {total_pages} pages in PDF")
            
            # Parse page range
            pages_to_convert = self.parse_page_range(page_range, total_pages)
            actual_pages_to_convert = len(pages_to_convert)
            
            os.makedirs(output_folder, exist_ok=True)
            
            converted_count = 0
            for i, page_num in enumerate(pages_to_convert):
                if self.should_stop:
                    self.log_message("Conversion stopped by user")
                    break
                
                try:
                    self.log_message(f"Converting page {page_num}/{total_pages}...")
                    page_images = convert_from_path(
                        pdf_path,
                        dpi=dpi,
                        first_page=page_num,
                        last_page=page_num,
                        thread_count=1
                    )
                    
                    if page_images:
                        image_path = os.path.join(
                            output_folder, 
                            f"page_{str(page_num).zfill(len(str(total_pages)))}.{fmt}"
                        )
                        page_images[0].save(image_path, fmt.upper())
                        converted_count += 1
                        self.log_message(f"Successfully saved page {page_num}")
                    
                    # Clean up memory
                    del page_images
                    gc.collect()
                    
                except Exception as page_error:
                    self.log_message(f"Error converting page {page_num}: {str(page_error)}")
                
                # Update progress
                self.progress_var.set((i + 1) / actual_pages_to_convert * 100)
                self.root.update_idletasks()

            elapsed_time = time.time() - start_time
            if self.should_stop:
                self.log_message(
                    f"Conversion partially completed ({converted_count}/"
                    f"{actual_pages_to_convert} pages in {elapsed_time:.2f} seconds)"
                )
                messagebox.showinfo("Stopped", 
                    f"Converted {converted_count} of {actual_pages_to_convert} "
                    f"pages in {elapsed_time:.2f} seconds")
            else:
                self.log_message(
                    f"Conversion completed ({converted_count}/"
                    f"{actual_pages_to_convert} pages in {elapsed_time:.2f} seconds)"
                )
                messagebox.showinfo("Success", 
                    f"Converted {converted_count} of {actual_pages_to_convert} "
                    f"pages in {elapsed_time:.2f} seconds")

        except Exception as e:
            self.log_message(f"Fatal Error: {str(e)}")
            messagebox.showerror("Conversion Error", str(e))
        
        finally:
            self.progress_var.set(0)
            self.conversion_in_corso = False
            self.should_stop = False
            self.convert_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            gc.collect()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()