# EmphaTech Voice Banking API Documentation

## Overview
EmphaTech is a voice-first banking application with two main services:
- **Backend API** (Node.js) - Core banking operations
- **Voice Service** (Python/FastAPI) - Voice processing and conversation

---

## 🚀 Quick Start

### Backend API
- **Base URL**: `http://localhost:3000`
- **API Path**: `/api`
- **Content-Type**: `application/json`

### Voice Service
- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

---

## 📋 Backend API Endpoints

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

### 2. Get User Profile
```http
GET /api/user/profile
```

**Response:**
```json
{
  "userId": "user123",
  "firstName": "Empha",
  "accountNumber": "1234567890",
  "phoneNumber": "+2348123456789"
}
```

---

### 3. Get Account Balance
```http
GET /api/account/balance
```

**Response:**
```json
{
  "balance": 150000.00,
  "currency": "NGN",
  "accountNumber": "1234567890",
  "lastUpdated": "2024-01-15T10:30:00.000Z"
}
```

---

### 4. Get Banks List
```http
GET /api/banks/list
```

**Response:**
```json
{
  "banks": [
    {
      "name": "First Bank",
      "code": "011",
      "aliases": ["first bank", "fbn"]
    },
    {
      "name": "GTBank",
      "code": "058",
      "aliases": ["gt bank", "gee tee bank", "guaranty trust", "gtb"]
    },
    {
      "name": "UBA",
      "code": "033",
      "aliases": ["uba", "united bank for africa"]
    },
    {
      "name": "Access Bank",
      "code": "044",
      "aliases": ["access", "access bank"]
    }
  ]
}
```

---

### 5. Verify Account
```http
POST /api/account/verify
```

**Request Body:**
```json
{
  "accountNumber": "1234567890",
  "bankName": "GTBank",
  "requestId": "req_123"
}
```

**Response:**
```json
{
  "accountNumber": "1234567890",
  "bankName": "GTBank",
  "accountName": "Bola Okoro",
  "requestId": "req_123"
}
```

---

### 6. Create Transaction
```http
POST /api/transaction/create
```

**Request Body:**
```json
{
  "amount": 5000,
  "currency": "NGN",
  "recipientAccount": "0987654321",
  "recipientBank": "GTBank",
  "sessionId": "session_123"
}
```

**Response:**
```json
{
  "transactionId": "uuid-generated-id",
  "status": "pending"
}
```

**Error Response (Insufficient Funds):**
```json
{
  "error": "Insufficient funds"
}
```

---

### 7. Execute Transaction
```http
POST /api/transaction/execute
```

**Request Body:**
```json
{
  "transactionId": "uuid-generated-id",
  "pinVerified": true,
  "finalConfirmation": true
}
```

**Response:**
```json
{
  "transactionId": "uuid-generated-id",
  "status": "successful"
}
```

**Error Response:**
```json
{
  "error": "Verification failed"
}
```

---

### 8. Get Transaction Status
```http
GET /api/transaction/status/:transactionId
```

**Response:**
```json
{
  "transactionId": "uuid-generated-id",
  "status": "successful",
  "newBalance": 145000.00,
  "referenceNumber": "T123456789",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "errorMessage": null
}
```

---

## 🎤 Voice Service Endpoints

### 1. Voice Authentication
```http
POST /voice/authenticate
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "phrase": "expected phrase",
  "deviceId": "device_123"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "spoken text",
  "phrase": "expected phrase",
  "deviceId": "device_123"
}
```

---

### 2. Announce Balance
```http
POST /voice/announce-balance
```

**Request Body:**
```json
{
  "userId": "user123",
  "userName": "Empha",
  "includeWelcome": true,
  "voiceSpeed": "normal",
  "voiceId": "Joanna",
  "balance": 150000.00
}
```

**Response:**
```json
{
  "audio": "base64-encoded-mp3-audio"
}
```

---

### 3. Process Voice Command
```http
POST /voice/process-command
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "sessionId": "session_123",
  "context": {}
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "balance",
  "intent": "get_balance",
  "balance": 150000.00,
  "currency": "NGN",
  "message": "Your balance is 150000 NGN.",
  "sessionId": "session_123",
  "context": {}
}
```

---

### 4. Confirm Amount
```http
POST /voice/confirm-amount
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "expectedAmount": 5000,
  "spokenAmount": "five thousand"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "five thousand",
  "expectedAmount": 5000,
  "spokenAmount": "five thousand"
}
```

---

### 5. Capture Account
```http
POST /voice/capture-account
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "accountType": "savings",
  "partialNumber": "123",
  "context": "transfer"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "1234567890",
  "accountType": "savings",
  "partialNumber": "123",
  "context": "transfer"
}
```

---

### 6. Recognize Bank
```http
POST /voice/recognize-bank
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "spokenBank": "GTBank",
  "context": "transfer"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "GTBank",
  "spokenBank": "GTBank",
  "context": "transfer"
}
```

---

### 7. Verify PIN
```http
POST /voice/verify-pin
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "transactionId": "uuid-generated-id",
  "sessionId": "session_123"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "one two three four",
  "transactionId": "uuid-generated-id",
  "sessionId": "session_123"
}
```

---

### 8. Final Confirmation
```http
POST /voice/final-confirmation
```

**Request Body:**
```json
{
  "transactionId": "uuid-generated-id",
  "amount": 5000,
  "recipientName": "Bola Okoro",
  "recipientBank": "GTBank",
  "accountNumber": "1234567890",
  "voiceId": "Joanna"
}
```

**Response:**
```json
{
  "audio": "base64-encoded-mp3-audio"
}
```

---

### 9. Get Available Voices
```http
GET /voice/available-voices
```

**Response:**
```json
{
  "voices": [
    {
      "id": "Joanna",
      "name": "Joanna",
      "gender": "Female",
      "language": "US English",
      "supportedEngines": ["neural", "standard"]
    }
  ]
}
```

---

### 10. Welcome After Login
```http
POST /voice/welcome-after-login
```

**Request Body:**
```json
{
  "userId": "user123",
  "userName": "Empha",
  "voiceId": "Joanna",
  "voiceSpeed": "medium"
}
```

**Response:**
```json
{
  "status": "success",
  "sessionId": "user-user123-1234567890",
  "prompt": "Welcome back Empha! Your current balance is one hundred and fifty thousand Naira. How may I help you today? You can say 'transfer money', 'check balance', 'purchase airtime', or 'purchase data'.",
  "prompt_audio": "base64-encoded-mp3-audio",
  "step": "awaiting_action"
}
```

### 11. Voice Conversation (Main Endpoint)
```http
POST /voice/converse
```

**Request Body:**
```json
{
  "voiceData": "base64-encoded-mp3-audio",
  "sessionId": "session_123"
}
```

**Response:**
```json
{
  "status": "success",
  "transcript": "transfer",
  "prompt": "Kindly state the account number.",
  "prompt_audio": "base64-encoded-mp3-audio",
  "step": "awaiting_account"
}
```

---

## 🎯 Voice Conversation Flow

### Testing Script - What to Say:

1. **Say "transfer"** → System: "Kindly state the account number."
2. **Say "1234567890"** → System: "Which bank?"
3. **Say "GTBank"** → System: "How much would you like to send to Bola Okoro at GTBank?"
4. **Say "five thousand"** → System: "Please state your four digit PIN."
5. **Say "one two three four"** → System: "Please confirm, you want to send five thousand Naira to Bola Okoro at GTBank, account number 1234567890. Say 'send' to confirm."
6. **Say "send"** → System: "Transaction successful!"

### Hardcoded Values:
- **Account Number**: `1234567890`
- **Bank**: `GTBank`
- **Account Name**: `Bola Okoro`
- **Amount**: `five thousand` (₦5,000)
- **PIN**: Any 4 digits (not verified)

---

## ⚠️ Error Handling

### HTTP Status Codes:
- **200**: Success
- **400**: Bad Request (invalid data, insufficient funds)
- **404**: Not Found (transaction, user)
- **500**: Server Error

### Common Error Responses:
```json
{
  "error": "Insufficient funds"
}
```

```json
{
  "error": "Transaction not found"
}
```

```json
{
  "error": "Verification failed"
}
```

---

## 🔧 Setup Instructions

### Backend (Node.js):
```bash
cd EmphaTech
npm install
npm start
```

### Voice Service (Python):
```bash
cd Python_voice_service
pip install -r requirements.txt
uvicorn app:app --reload
```

### Environment Variables:
Create `.env` file in both directories:
```env
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
```

---

## 📝 Notes

- All endpoints are for demo/hackathon purposes
- User ID is hardcoded as `user123`
- Current balance: ₦150,000.00
- Voice service requires AWS Polly for TTS
- Audio must be base64-encoded MP3 format
- Session management is in-memory (resets on server restart)