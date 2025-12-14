# NAS Migration System

A real-time file organization system with deep content extraction, automatic classification, and a modern macOS-style dashboard.

## Features

- **Deep Content Extraction**: Extracts full text from PDFs, images (OCR), and documents
- **Auto-Classification**: Categorizes files into Career, Academic, Projects, Financial
- **Real-time Sync**: Automatically detects new files and updates the dashboard
- **Secure Dashboard**: FastAPI backend with OAuth2 + React frontend
- **macOS Finder UI**: Clean, native-looking interface

## Setup

### Backend
```bash
cd NAS_Migration_PoC
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend && uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Backend runs on `http://localhost:8000`
2. Frontend runs on `http://localhost:3000`
3. Login: `admin` / `secret`
4. Drop files into `~/Downloads` - they'll auto-sync!

## Tech Stack

- **Backend**: FastAPI, Watchdog, PyMuPDF, Tesseract
- **Frontend**: React, TypeScript, Tailwind CSS v4, Vite
- **Real-time**: WebSockets

## AI File Organization

This project includes an AI-powered organizer that uses Google's Gemini 2.5 Flash model to intelligently categorize your files.

### Setup
1. Get a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. Install the new SDK:
   ```bash
   pip install -U google-genai
   ```

### Usage
1. First, extract file content:
   ```bash
   python main.py
   ```
2. Run the AI Organizer:
   ```bash
   export GEMINI_API_KEY="your_api_key"
   python ai_organize.py
   ```

The script will:
1. Analyze your file content and metadata.
2. Generate a smart folder structure (e.g., `Academic`, `Financial`, `Career`).
3. **Move** files from your source (Downloads) to `AI_Organized_Files`.

