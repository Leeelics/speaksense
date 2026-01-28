from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import whisper
import re
import os
import tempfile
from typing import Dict, List
from pathlib import Path

app = FastAPI(title="SpeakSense", description="AI Speech Analysis Tool")

# Load Whisper model
model = whisper.load_model("base")

# Get template directory relative to this file
template_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(template_dir))

# Speech filler patterns
FILLERS = [
    r'\b(um|uh|er|ah)\b',
    r'\b(like|you know|so|actually)\b',
    r'\b(basically|literally|obviously)\b'
]

def analyze_speech(text: str) -> Dict:
    """Analyze speech for fillers and basic metrics"""
    words = text.split()
    total_words = len(words)
    
    # Count fillers
    filler_count = 0
    filler_details = {}
    
    for pattern in FILLERS:
        matches = re.findall(pattern, text.lower())
        if matches:
            for match in matches:
                filler_details[match] = filler_details.get(match, 0) + 1
                filler_count += 1
    
    # Calculate metrics
    filler_rate = (filler_count / total_words * 100) if total_words > 0 else 0
    
    return {
        "total_words": total_words,
        "filler_count": filler_count,
        "filler_rate": round(filler_rate, 2),
        "filler_details": filler_details,
        "transcript": text
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """Analyze uploaded audio file"""
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Transcribe audio
        result = model.transcribe(tmp_file_path)
        transcript = result["text"]
        
        # Analyze speech
        analysis = analyze_speech(transcript)
        
        return {
            "success": True,
            "analysis": analysis
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
    finally:
        # Clean up temp file
        os.unlink(tmp_file_path)

def main():
    """Entry point for the application"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
