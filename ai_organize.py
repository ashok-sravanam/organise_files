"""
AI-Powered File Organization Module using Google Gemini 2.5

This module:
1. Reads the extracted file data from migration_index.json
2. Sends it to Gemini 2.5 Flash to suggest optimal folder structure
3. Applies the AI's recommendations to organize files
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List
import shutil

# Import the new Google GenAI SDK
from google import genai
from google.genai import types

# Add NAS_Migration_PoC to path for importing src modules
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
# Also try adding the nested directory if it exists (for the organized structure)
if (BASE_DIR / "NAS_Migration_PoC").exists():
    sys.path.append(str(BASE_DIR / "NAS_Migration_PoC"))

try:
    from src.organizer import FileOrganizer
except ImportError:
    # Fallback if src is not found directly
    try:
        from NAS_Migration_PoC.src.organizer import FileOrganizer
    except ImportError:
        print("Error: Could not import FileOrganizer. Please ensure 'src' module is in python path.")
        sys.exit(1)

class AIOrganizer:
    def __init__(self, index_path: Path, api_key: str):
        self.index_path = index_path
        # Initialize the new GenAI client
        self.client = genai.Client(api_key=api_key)
        # User explicitly requested gemini-2.5-flash
        self.model_name = "gemini-2.5-flash"

    def load_index(self) -> List[Dict]:
        """Load the extracted file data."""
        if not self.index_path.exists():
            return []
        with open(self.index_path, 'r') as f:
            return json.load(f)
    
    def prepare_summary_for_ai(self, documents: List[Dict]) -> str:
        """Create a concise summary of files for AI analysis."""
        summary = "# File Inventory for Organization\n\n"
        
        # Group by current category to give context
        by_category = {}
        for doc in documents:
            cat = doc.get('category', 'Uncategorized')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                'filename': doc['filename'],
                'subfolder': doc.get('subfolder', ''),
            })
        
        for category, files in by_category.items():
            summary += f"\n## {category} ({len(files)} files)\n"
            for file in files:
                summary += f"- {file['filename']}"
                if file['subfolder']:
                    summary += f" (Current: {file['subfolder']})"
                summary += "\n"
        
        return summary
    
    def get_ai_suggestions(self, documents: List[Dict]) -> Dict:
        """Ask Gemini AI to suggest optimal folder organization."""
        summary = self.prepare_summary_for_ai(documents)
        
        prompt = f"""You are an expert file organization assistant. Analyze this file inventory and suggest an optimal folder structure.

{summary}

Total files to organize: {len(documents)}

Create a smart, hierarchical folder structure (max 3 levels) that makes sense for these files.
Identify clusters of related files (e.g. "Tax Documents", "Resumes", "School Projects", "Invoices").

IMPORTANT: Respond ONLY with valid JSON in this exact format:

{{
  "folder_structure": {{
    "CategoryName": {{
      "SubFolder": "description"
    }}
  }},
  "file_mapping": {{
    "exact_filename.ext": "CategoryName/SubFolder"
  }},
  "summary": "Brief explanation"
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            # Try fallback without json mode if that failed
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt + "\n\nResponse must be valid JSON."
            )
            text = response.text
            # Clean markdown
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "")
            return json.loads(text)

    def apply_organization(self, suggestions: Dict, destination_root: Path):
        """Apply AI's suggested organization."""
        destination_root.mkdir(parents=True, exist_ok=True)
        
        file_mapping = suggestions.get('file_mapping', {})
        docs = self.load_index()
        # Create normalized map: lowercase -> doc
        doc_map = {d['filename'].lower().strip(): d for d in docs}
        
        # DEBUG: Save AI response
        with open("ai_response.json", "w") as f:
            json.dump(suggestions, f, indent=2)
            
        print(f"DEBUG: Index contains {len(docs)} files.")
        print(f"DEBUG: AI suggested moving {len(file_mapping)} files.")
        
        # DEBUG: Print first 5 mapping keys to see what AI returned
        first_keys = list(file_mapping.keys())[:5]
        print(f"DEBUG: First 5 AI keys: {first_keys}")
        
        organized_count = 0
        from difflib import get_close_matches
        
        for i, (filename, suggested_path) in enumerate(file_mapping.items()):
            key = filename.lower().strip()
            
            # Debug first one detailedly
            if i == 0:
                print(f"DEBUGGING MATCH for: '{filename}' (key: '{key}')")
                if key in doc_map:
                    print("   -> Exact string match found in doc_map keys.")
                else:
                    print("   -> No exact string match.")
            
            # 1. Exact Normal Match
            doc = doc_map.get(key)
            
            # 2. URL Decode Match (if needed)
            if not doc:
                import urllib.parse
                decoded = urllib.parse.unquote(key)
                doc = doc_map.get(decoded)
            
            # 3. Fuzzy Match
            if not doc:
                matches = get_close_matches(key, doc_map.keys(), n=1, cutoff=0.8)
                if matches:
                    doc = doc_map[matches[0]]
                    print(f"   (Fuzzy matched '{filename}' to '{matches[0]}')")
            
            if doc:
                source = None
                if 'original_file_path' in doc:
                    source = Path(doc['original_file_path'])
                
                # Fallback to Downloads if path is missing or doesn't exist
                if not source or not source.exists():
                     alt_source = Path("/Users/ashoks/Downloads") / filename
                     if alt_source.exists():
                         source = alt_source
                     else:
                         # Try unnormalized filename from doc if available
                         raw_name = doc.get('filename')
                         if raw_name:
                             alt_source_2 = Path("/Users/ashoks/Downloads") / raw_name
                             if alt_source_2.exists():
                                 source = alt_source_2
                
                if not source or not source.exists():
                    print(f"⚠️  Source file missing: {filename} (checked path and Downloads)")
                    continue
                    
                dest_folder = destination_root / suggested_path
                dest_folder.mkdir(parents=True, exist_ok=True)
                dest_file = dest_folder / filename
                
                try:
                    # Check if destination already exists to avoid overwriting or redundant copy
                    if dest_file.exists():
                        # Verify size match before assuming it's the same
                        if dest_file.stat().st_size == source.stat().st_size:
                            print(f"✓ Skipped (exists): {filename}")
                            # Track for cleanup
                            if source.exists():
                                self.cleanup_source(source)
                            organized_count += 1
                            continue
                            
                    shutil.copy2(source, dest_file)
                    organized_count += 1
                    print(f"✓ Copied: {filename}")
                    
                    # Cleanup source after successful copy
                    self.cleanup_source(source)
                    
                except Exception as e:
                    print(f"✗ Failed move {filename}: {e}")
            else:
                 print(f"⚠️  No match for: '{filename}'")
        
        return organized_count
    
    def cleanup_source(self, source_path: Path):
        """Safely remove the source file."""
        try:
            # specialized safety check for Downloads
            if "Downloads" in str(source_path) and source_path.exists():
                os.remove(source_path)
                print(f"   🗑️  Removed original: {source_path.name}")
        except Exception as e:
            print(f"   ⚠️ Could not remove source: {e}")


if __name__ == "__main__":
    # Configure paths
    BASE_DIR = Path(__file__).resolve().parent
    
    # Check multiple locations for index file due to folder structure ambiguity
    POSSIBLE_INDEX_LOCATIONS = [
        BASE_DIR / "migration_index.json",
        BASE_DIR / "NAS_Migration_PoC" / "migration_index.json"
    ]
    
    INDEX_FILE = None
    for path in POSSIBLE_INDEX_LOCATIONS:
        if path.exists():
            INDEX_FILE = path
            break
            
    if not INDEX_FILE:
        print("❌ Could not find migration_index.json. Please run main.py first.")
        # Attempt to find main.py to hint user
        sys.exit(1)
        
    DEST_DIR = Path("/Users/ashoks/Downloads/AI_Organized_Files")
    API_KEY = "REDACTED_API_KEY" # User provided key
    
    print(f"🤖 AI-Powered File Organization using {INDEX_FILE}")
    print("=" * 60)
    
    organizer = AIOrganizer(INDEX_FILE, API_KEY)
    
    print("\n📊 Loading extracted file data...")
    documents = organizer.load_index()
    print(f"   Found {len(documents)} files")
    
    if len(documents) == 0:
        print("   No files to organize.")
        sys.exit(0)
    
    print(f"\n🧠 Asking Gemini ({organizer.model_name}) for organization suggestions...")
    
    try:
        suggestions = organizer.get_ai_suggestions(documents)
        
        print("\n📁 AI's Suggested Folder Structure:")
        print("-" * 60)
        for main_folder, subfolders in suggestions.get('folder_structure', {}).items():
            print(f"\n{main_folder}/")
            if isinstance(subfolders, dict):
                for subfolder, desc in subfolders.items():
                    print(f"  ├── {subfolder}/")
        
        print("\n" + "=" * 60)
        print(suggestions.get('summary', 'Organization complete'))
        print("=" * 60)
        
        print(f"\n📦 Applying organization to {DEST_DIR}...")
        count = organizer.apply_organization(suggestions, DEST_DIR)
        
        print(f"\n✅ Successfully organized {count} files!")
        print(f"   Check your files at: {DEST_DIR}")
        
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        import traceback
        traceback.print_exc()
