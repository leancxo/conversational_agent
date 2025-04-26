# Conversational Agent

A real-time conversational agent that uses the Dia model for speech synthesis and natural language processing.

## Features

- Real-time speech synthesis using Dia model
- WebSocket-based communication
- Error handling and resource cleanup
- Configurable settings via environment variables

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/conversational-agent.git
cd conversational-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:
```
DIA_MODEL_PATH=/path/to/your/dia/model
```

## Usage

1. Start the server:
```bash
python src/main.py
```

2. The server will start on `http://localhost:8000` by default.

3. Connect to the WebSocket endpoint at `ws://localhost:8000/ws` to start a conversation.

## API Endpoints

- `GET /`: Health check endpoint
- `GET /ws`: WebSocket endpoint for real-time communication

## Error Handling

The agent includes comprehensive error handling for:
- Model initialization failures
- Speech generation errors
- WebSocket connection issues
- Resource cleanup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 