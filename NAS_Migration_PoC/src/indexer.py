import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentIndexer:
    def __init__(self, output_path="full_content_index.json"):
        self.output_path = Path(output_path)
        self.index = []

    def add_document(self, doc_data, classification):
        """
        Add a document to the in-memory index.
        doc_data: dict containing metadata and extracted text
        classification: dict containing category, subfolder, confidence
        """
        entry = {
            "id": len(self.index) + 1,
            "filename": doc_data.get("filename"),
            "original_path": doc_data.get("original_file_path"),
            "file_type": doc_data.get("file_type"),
            "file_size": doc_data.get("file_size"),
            "file_date": doc_data.get("file_date"),
            "category": classification.get("service_category"),
            "subfolder": classification.get("subfolder_path"),
            "confidence": classification.get("confidence_score"),
            "tags": classification.get("reasoning", "").split(". "), # Simple tag extraction from reasoning
            "extracted_text_preview": doc_data.get("extracted_text", "")[:200], # Preview for quick UI
            "full_text": doc_data.get("extracted_text", "") # Store full text for search
        }
        self.index.append(entry)

    def save(self):
        """Save the index to a JSON file."""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, default=str)
            logger.info(f"Successfully saved index with {len(self.index)} documents to {self.output_path}")
            return str(self.output_path)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise
