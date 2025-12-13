import shutil
from pathlib import Path
from src.config import NEW_NAS_PATH

class FileOrganizer:
    def __init__(self, base_dest_path=NEW_NAS_PATH):
        self.base_dest_path = Path(base_dest_path)

    def organize(self, file_path, classification):
        """Copy file to new location based on classification."""
        category = classification.get("service_category", "Miscellaneous")
        subfolder = classification.get("subfolder_path", "Uncategorized")
        
        # Construct destination path
        dest_dir = self.base_dest_path / category / subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        filename = Path(file_path).name
        dest_path = dest_dir / filename
        
        # Handle duplicates
        counter = 1
        while dest_path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1
            
        try:
            shutil.copy2(file_path, dest_path)
            return dest_path
        except Exception as e:
            raise IOError(f"Failed to copy file: {e}")
