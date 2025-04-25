from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import logging
from pathlib import Path
import json
from .ai.dia_agent import DiaAgent
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Conversational Agent")

# Initialize Dia agent
dia_agent = DiaAgent()

# Mount static files
static_path = Path(__file__).parent / "ui" / "static"
static_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "ui" / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Conversational Agent"}
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time chat."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                # Parse the incoming message
                message_data = json.loads(data)
                text = message_data.get('text', '')
                require_audio = message_data.get('require_audio', False)
                
                # Process message using DiaAgent
                response_text = dia_agent.process_message(text)
                
                # Generate audio if requested
                audio_path = None
                if require_audio:
                    try:
                        audio_path = dia_agent.generate_speech(response_text)
                        # Extract just the filename from the path
                        audio_path = os.path.basename(audio_path)
                    except Exception as e:
                        logger.error(f"Failed to generate speech: {e}")
                
                # Send response
                response = {
                    'text': response_text,
                    'audio_path': audio_path
                }
                await websocket.send_text(json.dumps(response))
                
            except json.JSONDecodeError:
                logger.error("Failed to parse message as JSON")
                await websocket.send_text(json.dumps({
                    'text': "Error: Invalid message format",
                    'audio_path': None
                }))
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/chat")
async def chat(message: dict):
    """Handle chat messages via HTTP POST."""
    try:
        response_text = f"Echo: {message.get('message', '')}"
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"error": "Failed to process message"}

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files."""
    import tempfile
    audio_path = Path(tempfile.gettempdir()) / filename
    if audio_path.exists():
        return FileResponse(audio_path, media_type="audio/mpeg")
    return {"error": "Audio file not found"}

def main():
    """Main entry point of the application."""
    logger.info("Starting Conversational Agent...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 