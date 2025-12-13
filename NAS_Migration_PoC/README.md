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
