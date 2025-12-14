# NAS Migration System - Proof of Concept

An intelligent file organization system that extracts content from documents, uses AI to suggest optimal folder structures, and automatically organizes files.

## Quick Start

**See [SETUP.md](./SETUP.md) for detailed installation instructions.**

```bash
# Backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements_fixed.txt
python -m uvicorn backend.main:app --reload --port 8005

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

## Features
- **Deep Content Extraction**: Reads PDFs, images, and documents using OCR
- **AI-Powered Organization**: Uses Google Gemini 2.5 Flash to intelligently categorize files
- **Real-time Dashboard**: macOS Finder-inspired UI built with React
- **Auto-Sync**: Watches for new files and automatically processes them dashboard
- **Secure Dashboard**: FastAPI backend with OAuth2 + React frontend
- **macOS Finder UI**: Clean, native-looking interface

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

