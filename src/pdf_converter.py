import os
import gc
from pdf2image import convert_from_path
from pdf2image.pdf2image import pdfinfo_from_path

class PDFConverterEngine:
    def __init__(self):
        self.conversion_active = False
        self.should_stop = False
    
    def parse_page_range(self, page_range_str, max_pages):
        """Parse the page range selection string"""
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
    
    def convert_page(self, pdf_path, page_num, dpi, output_folder, fmt, total_pages, log_callback):
        """Convert a single page"""
        try:
            log_callback(f"Converting page {page_num}/{total_pages}...")
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
                log_callback(f"Successfully saved page {page_num}")
                return True
            
        except Exception as e:
            log_callback(f"Error converting page {page_num}: {str(e)}")
            return False
        finally:
            gc.collect()