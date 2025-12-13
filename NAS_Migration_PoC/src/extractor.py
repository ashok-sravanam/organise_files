import os
from pathlib import Path
import logging

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
try:
    from PIL import Image
    import pytesseract
except ImportError:
    pytesseract = None
    Image = None

logger = logging.getLogger(__name__)

class ContentExtractor:
    def extract(self, file_path):
        """Extract text and metadata from file."""
        file_path = Path(file_path)
        stats = file_path.stat()
        
        metadata = {
            "filename": file_path.name,
            "file_size": stats.st_size,
            "file_date": stats.st_mtime,
            "file_type": file_path.suffix.lower().lstrip('.')
        }
        
        text_content = ""
        
        try:
            if metadata["file_type"] == "txt":
                text_content = file_path.read_text(errors='ignore')
            elif metadata["file_type"] == "pdf":
                if fitz:
                    try:
                        with fitz.open(file_path) as doc:
                            # Extract text from first 5 pages to keep it performant but detailed
                            for i, page in enumerate(doc):
                                if i > 5: break 
                                text_content += page.get_text() + "\n"
                    except Exception as e:
                        logger.warning(f"PyMuPDF failed for {file_path}: {e}")
                        text_content = "[PDF Error]"
                else:
                    text_content = "[PDF Extraction Placeholder - PyMuPDF missing]"
            elif metadata["file_type"] in ["png", "jpg", "jpeg", "tiff"]:
                if pytesseract and Image:
                    try:
                        text_content = pytesseract.image_to_string(Image.open(file_path))
                    except Exception as e:
                        text_content = f"[OCR Error: {e}]"
                else:
                    text_content = "[Image OCR Placeholder - Tesseract/PIL missing]"
            elif metadata["file_type"] in ["py", "js", "ts", "html", "css", "json", "sql", "md"]:
                # Code files - read as text
                text_content = file_path.read_text(errors='ignore')
            else:
                text_content = f"[Unsupported file type: {metadata['file_type']}]"
        except Exception as e:
            text_content = f"[Extraction Error: {str(e)}]"

        return text_content, metadata
