# Strands Agent Web App

A clean web interface for interacting with Strands AI agents with auto-approval for mutations.

## Project Structure

```
Strands_poc/
├── __init__.py          # Package initialization
├── app.py              # Main application (recommended)
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── [other files]      # 
```

## Prerequisites

- **Python 3.10+**
- **Strands SDK and Tools**

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser:
```
http://localhost:8018
```

## Features

- **Auto-approval mode** - No confirmation prompts for mutations
- **Clean interface** - Simple form-based interaction
- **Real-time processing** - Loading indicators and immediate feedback
- **Error handling** - Clear error messages
- **Tool integration** - Calculator, AWS, and file operations

## Available Tools

- **Calculator** - Mathematical operations
- **AWS Tools** - Cloud service interactions
- **File Operations** - Read/write file operations

## Configuration

The app automatically sets `BYPASS_TOOL_CONSENT=true` for seamless operation without confirmation prompts.

## Usage Notes

- All operations are auto-approved
- No confirmation dialogs will appear
- Suitable for trusted environments
- Check console output for detailed logs