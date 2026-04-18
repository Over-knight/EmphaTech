# EmphaTech - Accessible Banking Platform

An innovative banking platform designed with accessibility at its core, enabling users to perform financial transactions through both traditional UI and voice-based interactions. Built with a modern tech stack of Node.js, React, and Python.

## Overview

EmphaTech is a full-stack web application that provides a secure and user-friendly banking experience with voice-enabled features. The platform allows users to manage their accounts, perform transactions, and interact with the system using voice commands by leveraging OpenAI's Whisper for speech recognition and Amazon Polly for text-to-speech.

## Features

- **User Account Management**: View profile information and account balance
- **Transaction Management**: Create, execute, and track transaction status
- **Money Transfer**: Send money between accounts
- **Recharge Services**: Top-up accounts with recharge cards
- **Bank Integration**: Access a comprehensive list of partner banks
- **Voice Interface**: Interact with the platform using voice commands
  - Speech-to-text transcription via Whisper
  - Text-to-speech responses via Amazon Polly
- **Real-time UI Updates**: Voice indicator, transcript display, and transaction panel updates
- **Responsive Design**: Tailwind CSS powered UI that adapts to all screen sizes
- **API Health Monitoring**: Built-in health check endpoints

## Tech Stack

### Backend
- **Runtime**: Node.js (ES6 Modules)
- **Framework**: Express.js
- **Middleware**: CORS, body-parser
- **Deployment**: Vercel (serverless)
- **Additional**: UUID, dotenv for environment variables

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Post-processing**: PostCSS, Autoprefixer

### Voice Service
- **Framework**: FastAPI (Python)
- **Speech Recognition**: OpenAI Whisper
- **Text-to-Speech**: Amazon Polly
- **Audio Processing**: pydub, ffmpeg
- **AWS Integration**: boto3

## Project Structure

```
emphatech/
├── src/                          # Backend source code
│   ├── controllers/              # Business logic controllers
│   │   ├── AccountController.js
│   │   ├── BankController.js
│   │   ├── RechargeController.js
│   │   ├── SendController.js
│   │   ├── TransactionController.js
│   │   ├── UIController.js
│   │   ├── UserController.js
│   │   └── BaseController.js
│   ├── models/                   # Data models
│   │   ├── Bank.js
│   │   ├── Transaction.js
│   │   └── User.js
│   ├── routes/                   # API route definitions
│   │   └── index.js
│   ├── middleware/               # Custom middleware
│   │   └── authMiddleware.js
│   ├── Python_voice_service/     # Voice service (FastAPI)
│   │   ├── app.py               # Main FastAPI application
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── run_conversation.py   # Voice conversation handler
│   │   ├── encode_audio.py       # Audio encoding utilities
│   │   ├── decode_audio.py       # Audio decoding utilities
│   │   └── test_tts.py          # Text-to-speech testing
│   ├── frontend/                 # React frontend
│   │   ├── src/
│   │   │   ├── pages/           # React page components
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Recharge.jsx
│   │   │   │   ├── Send.jsx
│   │   │   │   └── Transactions.jsx
│   │   │   ├── services/        # API integration services
│   │   │   │   └── api.js
│   │   │   ├── App.jsx
│   │   │   ├── main.jsx
│   │   │   └── index.css
│   │   ├── vite.config.js
│   │   ├── tailwind.config.cjs
│   │   └── package.json
│   ├── server.js                # Express server entry point
│   ├── vercel.json              # Vercel deployment config
│   └── package.json
├── api/                         # Serverless API functions (optional)
│   └── index.js
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+ for voice service
- ffmpeg for audio processing
- AWS credentials (for Polly)

### Backend Setup

1. Navigate to the src directory:
   ```bash
   cd src
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the `src` directory:
   ```env
   PORT=3000
   # Add other environment variables as needed
   ```

4. Start the development server:
   ```bash
   npm run dev          # With hot-reload via nodemon
   # or
   npm start            # Standard start
   ```

The server will be running at `http://localhost:3000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd src/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

### Voice Service Setup

1. Navigate to the Python service directory:
   ```bash
   cd src/Python_voice_service
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure ffmpeg path in `app.py` (Windows users):
   Update the `ffmpeg_bin_dir` variable to point to your ffmpeg installation

4. Set up AWS credentials for Polly in your environment or `.env` file

5. Run the FastAPI server:
   ```bash
   python app.py
   # or with uvicorn
   uvicorn app:app --reload
   ```

## API Endpoints

All API endpoints are prefixed with `/api`

### User Management
- `GET /api/user/profile` - Retrieve user profile information
- `GET /api/account/balance` - Get account balance

### Transactions
- `POST /api/transaction/create` - Create a new transaction
- `POST /api/transaction/execute` - Execute a pending transaction
- `GET /api/transaction/status/:transactionId` - Get transaction status

### Banking Services
- `POST /api/account/verify` - Verify account details
- `POST /api/recharge-card` - Purchase recharge card
- `POST /api/transaction/send-money` - Send money to another account
- `GET /api/banks/list` - Get list of partner banks

### UI Voice Interaction
- `POST /api/ui/transcript/update` - Update voice transcript display
- `POST /api/ui/voice-indicator/update` - Update voice input indicator
- `POST /api/ui/transaction-panel/update` - Update transaction panel info

### Health Check
- `GET /api/health` - API health status

## Development Workflow

### Running the Full Stack Locally

**Option 1: Terminal approach**
Open three terminals and run:
```bash
# Terminal 1: Backend
cd src && npm run dev

# Terminal 2: Frontend
cd src/frontend && npm run dev

# Terminal 3: Voice Service
cd src/Python_voice_service && python app.py
```

**Option 2: Using nodemon**
The backend is configured with nodemon for automatic restarts on file changes.

### CORS Configuration
The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:5173`

Update the `cors` configuration in `src/server.js` if you're running on different ports.

## Building for Production

### Frontend
```bash
cd src/frontend
npm run build
```

This generates a `dist` folder with optimized production build.

### Backend
The backend is ready for deployment as-is. It's configured for Vercel via `vercel.json`.

## Deployment

### Vercel Deployment
The project includes `vercel.json` configuration for serverless deployment:

1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Vercel will automatically detect and build the project
4. The backend will be deployed as a serverless function

### Environment Variables
Set the following in your deployment platform:
- `PORT` (if needed)
- AWS credentials for Polly (if using voice service)
- Any other required API keys

## Key Files

- **`src/server.js`** - Main Express server with middleware setup
- **`src/routes/index.js`** - Route definitions and controller initialization
- **`src/models/`** - Data model definitions
- **`src/controllers/`** - Business logic and request handlers
- **`src/frontend/src/App.jsx`** - Main React application component
- **`src/frontend/src/services/api.js`** - Centralized API client
- **`src/Python_voice_service/app.py`** - Voice service API

## CORS & Security

- CORS is enabled for localhost ports (3000, 5173)
- Body parser middleware handles JSON parsing
- Auth middleware is available in `src/middleware/authMiddleware.js`
- Environment variables are managed via dotenv

## Contributing

When making changes:
1. Follow the existing code structure and naming conventions
2. Controllers extend `BaseController`
3. Models define data structures
4. Routes are centralized in `routes/index.js`
5. Environment variables are loaded via dotenv

## Troubleshooting

### Port already in use
- Backend default: 3000
- Frontend default: 5173
- Specify different port with `PORT=<number>`

### CORS errors
- Ensure frontend and backend URLs match CORS configuration
- Check that both services are running

### Voice service issues
- Verify ffmpeg is installed and in PATH
- Check AWS credentials are set correctly
- Ensure all Python dependencies are installed

## License

ISC

## Support

For issues and bug reports, visit: https://github.com/Over-knight/EmphaTech/issues

## Repository

GitHub: https://github.com/Over-knight/EmphaTech