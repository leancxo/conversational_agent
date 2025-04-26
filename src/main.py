from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import uvicorn
import logging
from pathlib import Path
import json
from .ai.dia_model import DiaAgent
import os
import asyncio
from typing import Set

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console for now
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Voice Assistant")

# Initialize Dia agent
dia_agent = None

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()

# Mount static files
static_path = Path(__file__).parent / "ui" / "static"
static_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "ui" / "templates"))

@app.on_event("startup")
async def startup_event():
    global dia_agent
    try:
        logger.info("Initializing Voice Agent...")
        dia_agent = DiaAgent()
        logger.info("Voice Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Voice agent: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    if dia_agent:
        dia_agent.cleanup()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Voice Assistant"}
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time voice chat."""
    logger.info("New WebSocket connection attempt...")
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    active_connections.add(websocket)
    
    try:
        while True:
            try:
                logger.info("Waiting for message...")
                data = await websocket.receive_text()
                logger.info(f"Received message: {data}")
                
                try:
                    # Parse the incoming message
                    message_data = json.loads(data)
                    text = message_data.get('text', '')
                    
                    logger.info(f"Processing message: {text}")
                    # Process message using Voice Agent
                    response_text = dia_agent.process_message(text)
                    logger.info(f"Generated response: {response_text}")
                    
                    # Always generate audio for responses
                    audio_path = None
                    error_message = None
                    try:
                        logger.info("Generating speech...")
                        audio_path = dia_agent.generate_speech(response_text)
                        # Verify the audio file exists
                        import tempfile
                        full_path = os.path.join(tempfile.gettempdir(), audio_path)
                        if not os.path.exists(full_path):
                            raise RuntimeError("Generated audio file not found")
                        if os.path.getsize(full_path) == 0:
                            raise RuntimeError("Generated audio file is empty")
                        logger.info(f"Speech generated successfully: {audio_path}")
                    except Exception as e:
                        logger.error(f"Failed to generate speech: {e}")
                        logger.exception("Full traceback:")
                        audio_path = None
                        error_message = f"Sorry, I couldn't generate the voice response: {str(e)}"
                    
                    # Send response
                    response = {
                        'text': response_text,
                        'audio_path': audio_path,
                        'error': error_message
                    }
                    logger.info(f"Sending response: {response}")
                    await websocket.send_text(json.dumps(response))
                    logger.info("Response sent successfully")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message as JSON: {e}")
                    await websocket.send_text(json.dumps({
                        'text': "I couldn't understand that message. Could you try again?",
                        'audio_path': None,
                        'error': "Invalid message format"
                    }))
                    
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        logger.exception("Full traceback:")
    finally:
        active_connections.remove(websocket)
        try:
            await websocket.close()
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "ready" if dia_agent else "not_initialized"}

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files."""
    import tempfile
    audio_path = Path(tempfile.gettempdir()) / filename
    logger.info(f"Requested audio file: {audio_path}")
    
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        return JSONResponse(
            status_code=404,
            content={"error": "Audio file not found"}
        )
        
    if audio_path.stat().st_size == 0:
        logger.error(f"Audio file is empty: {audio_path}")
        return JSONResponse(
            status_code=500,
            content={"error": "Audio file is empty"}
        )
        
    logger.info("Audio file found and valid, serving...")
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={
            "Cache-Control": "no-cache",
            "X-Content-Type-Options": "nosniff"
        }
    )

def main():
    """Main entry point of the application."""
    logger.info("Starting Conversational Agent...")
    # Use a different port if 8000 is in use
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except OSError:
        logger.info("Port 8000 in use, trying port 8001")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )

if __name__ == "__main__":
    main() 