# Setup Guide

This guide will help you set up the NAS Migration PoC project from scratch.

## Prerequisites

- Python 3.13+ (recommended) or Python 3.10+
- Node.js 18+ and npm
- Tesseract OCR (for PDF text extraction)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd NAS_Migration_PoC/NAS_Migration_PoC
```

### 2. Backend Setup

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements_fixed.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Running the Application

### Start the Backend

From the project root (`NAS_Migration_PoC/NAS_Migration_PoC`):

```bash
# Make sure venv is activated
source venv/bin/activate

# Start the FastAPI server
python -m uvicorn backend.main:app --reload --port 8005
```

The backend will be available at: http://127.0.0.1:8005

### Start the Frontend

In a new terminal, from the project root:

```bash
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:5173 (or the port shown in terminal)

## Default Login Credentials

- **Username:** `admin`
- **Password:** `secret`

## AI File Organization

To use the AI-powered file organization feature:

```bash
# Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

# Run the organizer
python ai_organize.py
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`, ensure:
1. You're using the virtual environment (`source venv/bin/activate`)
2. You're running commands from the correct directory (`NAS_Migration_PoC/NAS_Migration_PoC`)
3. You're using `python -m uvicorn` instead of just `uvicorn`

### CORS Errors

The backend is configured to accept requests from:
- http://localhost:3000
- http://localhost:5173-5175
- http://127.0.0.1:3000
- http://127.0.0.1:5173-5175

If your frontend runs on a different port, update `backend/main.py` line 127.

### Port Already in Use

If port 8005 is already in use, change the port number:
```bash
python -m uvicorn backend.main:app --reload --port 8006
```

Then update the frontend API URL in `frontend/src/App.tsx` (line 15).
