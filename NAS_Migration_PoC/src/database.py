import sqlite3
import json
from datetime import datetime
from src.config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        self.connect()
        
        # Documents Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_file_path TEXT NOT NULL,
                new_file_path TEXT,
                filename TEXT,
                file_type TEXT,
                file_size INTEGER,
                file_date TIMESTAMP,
                service_category TEXT,
                subfolder_path TEXT,
                document_type TEXT,
                extracted_text TEXT,
                confidence_score INTEGER,
                processing_status TEXT,
                processed_timestamp TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Processing Log Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                original_path TEXT,
                new_path TEXT,
                confidence_score INTEGER,
                status TEXT,
                error_message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        self.close()

    def insert_document(self, doc_data):
        self.connect()
        sql = """
            INSERT INTO documents (
                original_file_path, filename, file_type, file_size, file_date,
                processing_status, processed_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        vals = (
            str(doc_data['original_file_path']),
            doc_data['filename'],
            doc_data['file_type'],
            doc_data['file_size'],
            doc_data['file_date'],
            'pending',
            datetime.now()
        )
        self.cursor.execute(sql, vals)
        doc_id = self.cursor.lastrowid
        self.conn.commit()
        self.close()
        return doc_id

    def update_document_classification(self, doc_id, classification_result):
        self.connect()
        sql = """
            UPDATE documents SET
                service_category = ?,
                subfolder_path = ?,
                document_type = ?,
                extracted_text = ?,
                confidence_score = ?,
                processing_status = ?
            WHERE id = ?
        """
        status = 'processed' if classification_result.get('confidence_score', 0) >= 85 else 'review_needed'
        vals = (
            classification_result.get('service_category'),
            classification_result.get('subfolder_path'),
            classification_result.get('document_type'),
            classification_result.get('extracted_text'),
            classification_result.get('confidence_score'),
            status,
            doc_id
        )
        self.cursor.execute(sql, vals)
        self.conn.commit()
        self.close()

    def log_action(self, action, original_path, new_path, confidence, status, error_msg=""):
        self.connect()
        sql = """
            INSERT INTO processing_log (action, original_path, new_path, confidence_score, status, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        vals = (action, str(original_path), str(new_path), confidence, status, error_msg)
        self.cursor.execute(sql, vals)
        self.conn.commit()
        self.close()
