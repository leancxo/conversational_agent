# Conversational Agent

A real-time chat application with WebSocket support, text-to-speech capabilities, and a modern web interface.

## Features

- Real-time chat using WebSocket
- Text-to-speech support
- Voice input capability
- Modern, responsive UI
- FastAPI backend
- Pytest-based testing suite

## Setup

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/Conversational_Agent.git
cd Conversational_Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```

The application will be available at http://localhost:8000

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Project Structure

```
├── src/
│   ├── ai/              # AI components
│   ├── ui/              # Frontend files
│   │   ├── static/      # Static assets (CSS, JS)
│   │   └── templates/   # HTML templates
│   └── main.py          # FastAPI application
├── tests/               # Test suite
├── requirements.txt     # Project dependencies
└── setup.py            # Package configuration
```

## License

MIT 