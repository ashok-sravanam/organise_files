import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
# Real Downloads folder as source
OLD_NAS_PATH = Path("/Users/ashoks/Downloads") 
# Destination folder in Downloads
NEW_NAS_PATH = OLD_NAS_PATH / "Organized_Personal_Files"
DB_PATH = BASE_DIR / "migration.db"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
NEW_NAS_PATH.mkdir(exist_ok=True)
# OLD_NAS_PATH already exists (it's Downloads)

# Database
DB_CONNECTION_STRING = f"sqlite:///{DB_PATH}"

# Processing
BATCH_SIZE = 10
CONFIDENCE_THRESHOLD_AUTO_FILE = 85
CONFIDENCE_THRESHOLD_REVIEW = 60

# Services (Categories for Personal Files)
SERVICES = [
    "Academic",
    "Career",
    "Identity",
    "Financial",
    "Projects",
    "Miscellaneous"
]
