# EmphaTech Python Voice Service

A FastAPI-based voice service application that provides speech-to-text (STT) and text-to-speech (TTS) capabilities for the EmphaTech platform. This service enables voice authentication, command processing, and interactive voice conversations for banking operations.

## Features

- **Voice Authentication**: Authenticate users through voice recognition
- **Speech-to-Text**: Convert voice commands to text using OpenAI's Whisper model
- **Text-to-Speech**: Generate speech from text using Amazon Polly
- **Interactive Voice Conversations**: Process voice commands for banking operations like:
  - Checking account balance
  - Transferring money
  - Purchasing airtime
  - Purchasing data

## Requirements

- Python 3.8-3.11
- FFmpeg installed on your system
- AWS account with Polly access (for TTS features)

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

4. Make sure FFmpeg is installed and accessible in your PATH

## Usage

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `/voice/authenticate`: Authenticate users through voice
- `/voice/process-command`: Process voice commands
- `/voice/announce-balance`: Generate speech for balance announcements
- `/voice/confirm-amount`: Confirm transaction amounts
- `/voice/capture-account`: Capture account information
- `/voice/recognize-bank`: Recognize bank names
- `/voice/verify-pin`: Verify PIN numbers
- `/voice/final-confirmation`: Generate final transaction confirmation
- `/voice/available-voices`: Get available Amazon Polly voices
- `/voice/welcome-after-login`: Generate welcome message after login
- `/voice/converse`: Interactive voice conversation

## License

[MIT](LICENSE)