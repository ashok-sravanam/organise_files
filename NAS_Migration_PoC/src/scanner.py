import os
from pathlib import Path

class FileScanner:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def scan(self):
        """Recursively scan for files."""
        if not self.root_path.exists():
            raise FileNotFoundError(f"Root path {self.root_path} does not exist.")

        for root, dirs, files in os.walk(self.root_path):
            # Exclusion Logic
            if "Organized_Personal_Files" in root or "NAS_Migration_PoC" in root or ".gemini" in root or "com.replay.Replay" in root:
                continue
                
            for file in files:
                file_path = Path(root) / file
                # Skip hidden files
                if file.startswith('.'):
                    continue
                yield file_path
