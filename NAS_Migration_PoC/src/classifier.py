import json
import random

class DocumentClassifier:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def classify(self, text, metadata):
        """Classify document based on text and metadata."""
        if self.use_mock:
            return self._heuristic_classify(text, metadata)
        else:
            # TODO: Implement actual LLM call here
            pass
        
    def _heuristic_classify(self, text, metadata):
        """Content-based heuristic classification."""
        # Use full extracted text + filename
        text_lower = text.lower()
        filename_lower = metadata['filename'].lower()
        combined_text = f"{filename_lower} \n {text_lower}"
        
        # Default
        category = "Miscellaneous"
        subfolder = "Uncategorized"
        confidence = 40 # Lower default confidence
        
        # 1. Detect Names (Strong signal if found in filename, medium if in top of text)
        detected_name = "General"
        # Check filename first (strongest)
        if "ashok" in filename_lower or "ash " in filename_lower: detected_name = "Ashok"
        elif "bala" in filename_lower: detected_name = "Bala"
        elif "gowtham" in filename_lower: detected_name = "Gowthamsai"
        # Check content if not in filename (e.g. resume header)
        elif "ashok" in text_lower[:200]: detected_name = "Ashok"
        elif "bala chandra" in text_lower[:200]: detected_name = "Bala"
        
        # 2. Heuristics (Content-Aware)
        
        # Career: Look for Resume/CV specific sections
        if any(kw in filename_lower for kw in ["resume", "cv", "portfolio"]) or \
           (len(text_lower) > 50 and any(kw in text_lower for kw in ["education", "experience", "skills", "project", "activities"]) and "summary" in text_lower):
            category = "Career"
            subfolder = detected_name 
            confidence = 90
            
        # Academic: Assignments, transcripts, courses
        elif "assignment" in combined_text or "homework" in combined_text or \
             ("professor" in text_lower and "semester" in text_lower) or \
             "transcript" in combined_text or "university of" in text_lower:
            category = "Academic"
            if "assignment" in combined_text: subfolder = "Assignments"
            elif "lecture" in combined_text or "slides" in text_lower: subfolder = "Lectures"
            elif "sop" in combined_text or "statement of purpose" in text_lower: subfolder = "SOPs"
            else: subfolder = "General"
            confidence = 85

        # Identity: Official IDs, Passports
        elif any(kw in combined_text for kw in ["passport", "visa", "driving license", "aadhaar", "ssn", "social security"]):
            category = "Identity"
            subfolder = detected_name
            confidence = 95
            
        # Financial: Receipts, Taxes
        elif any(kw in combined_text for kw in ["tax returns", "w2", "1099", "invoice", "receipt", "payment success", "transaction id", "billing"]):
            category = "Financial"
            subfolder = "Receipts_Invoices"
            confidence = 88
            
        # Projects: Code identifiers
        elif metadata["file_type"] in ["py", "js", "ts", "html", "css", "sql", "json", "java", "cpp", "c"] or \
             "def " in text or "function" in text or "import " in text or "select * from" in text_lower:
            category = "Projects"
            subfolder = "Code_Assets"
            confidence = 90
            
        return {
            "service_category": category,
            "subfolder_path": subfolder,
            "document_type": "Unknown",
            "extracted_text": text, # Pass full text for indexing
            "confidence_score": confidence,
            "reasoning": f"Content match. Name detected: {detected_name}"
        }
