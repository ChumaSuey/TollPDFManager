import fitz  # PyMuPDF
from PIL import Image

class PDFHandler:
    def __init__(self):
        self.doc = None
        self.current_page_idx = 0
        self.path = None

    def open_pdf(self, path):
        try:
            if self.doc:
                self.doc.close()
            self.doc = fitz.open(path)
            self.path = path
            self.current_page_idx = 0
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False

    def get_page_count(self):
        if self.doc:
            return self.doc.page_count
        return 0

    def get_page_image(self, page_num, zoom=1.0):
        if not self.doc or page_num < 0 or page_num >= self.doc.page_count:
            return None
        
        page = self.doc.load_page(page_num)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    
    def close(self):
        if self.doc:
            self.doc.close()
            self.doc = None
