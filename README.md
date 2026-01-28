# SpeakSense

AI-powered speech analysis tool to improve presentation skills and reduce speech fillers.

## Features (MVP)
- Audio recording and transcription
- Speech filler detection ("um", "uh", "like", etc.)
- Basic speech analysis (pace, pauses)
- Simple web interface

## Tech Stack
- Backend: FastAPI + Python
- AI: OpenAI Whisper
- Frontend: HTML/JS (minimal)
- Package Management: uv

## Setup
```bash
# Install dependencies
uv sync

# Run the application
uv run speaksense

# Or run directly
uv run python -m speaksense.main
```

## Development
```bash
# Install dev dependencies
uv sync --dev

# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Run tests
uv run pytest
```

## Usage
1. Open http://localhost:8000
2. Record your speech
3. Get instant analysis

## Project Structure
```
speaksense/
├── src/speaksense/
│   ├── __init__.py
│   ├── main.py
│   └── templates/
│       └── index.html
├── pyproject.toml
└── README.md
```
