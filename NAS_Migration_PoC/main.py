from src.config import OLD_NAS_PATH, BASE_DIR
from src.database import DatabaseManager
from src.scanner import FileScanner
from src.extractor import ContentExtractor
from src.classifier import DocumentClassifier
from src.organizer import FileOrganizer
from src.indexer import ContentIndexer
from tqdm import tqdm
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting NAS Migration System PoC...")

    # Initialize Components
    scanner = FileScanner(OLD_NAS_PATH)
    extractor = ContentExtractor()
    classifier = DocumentClassifier(use_mock=True)
    indexer = ContentIndexer(output_path=BASE_DIR / "migration_index.json")

    logger.info("Scanning files...")
    files = list(scanner.scan())
    logger.info(f"Found {len(files)} files.")

    for file_path in tqdm(files, desc="Processing Files"):
        try:
            # 1. Extract (Deep content read)
            text, metadata = extractor.extract(file_path)
            
            # 2. Classify (Based on content)
            classification = classifier.classify(text, metadata)
            
            # 3. Add to Search Index (Primary Goal)
            doc_data = metadata.copy()
            doc_data['original_file_path'] = str(file_path)
            doc_data['extracted_text'] = text
            indexer.add_document(doc_data, classification)
            
            # 4. (Optional) DB Logging for Audit
            # We skip full DB insert to speed up for this new 'Indexer' mode, or just log basic status
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    # Save the master index
    saved_path = indexer.save()
    logger.info(f"Migration Index saved to: {saved_path}")

if __name__ == "__main__":
    main()
