
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import whisper
import tempfile
import os
import time
# Set ffmpeg/ffprobe path for pydub before importing AudioSegment
ffmpeg_bin_dir = r"C:\Users\Hp\Downloads\ffmpeg-7.0.2-essentials_build\ffmpeg-7.0.2-essentials_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_bin_dir
assert os.path.isfile(os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")), "ffmpeg.exe not found!"
assert os.path.isfile(os.path.join(ffmpeg_bin_dir, "ffprobe.exe")), "ffprobe.exe not found!"
from pydub import AudioSegment
AudioSegment.converter = os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")
AudioSegment.ffprobe   = os.path.join(ffmpeg_bin_dir, "ffprobe.exe")
from dotenv import load_dotenv
load_dotenv()
from num2words import num2words

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

origins = [
     "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Whisper model is loaded once for efficiency
whisper_model = whisper.load_model("base")

# Initialize Amazon Polly client
try:
    polly_client = boto3.client(
        'polly',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
except NoCredentialsError:
    print("Warning: AWS credentials not found. TTS features will not work.")
    polly_client = None

class VoiceAuthRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    phrase: str
    deviceId: str

# --- STT Endpoint: Transcribes voice to text ---
@app.post("/voice/authenticate")
async def voice_authenticate(request: VoiceAuthRequest):
    try:
        # Decode base64 audio and save as mp3
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            temp_mp3_path = temp_mp3.name

        # Now close the file before reading
        audio = AudioSegment.from_mp3(temp_mp3_path)
        # Transcribe with Whisper
        result = whisper_model.transcribe(temp_mp3_path)
        transcript = result["text"]
        return {
            "status": "success",
            "transcript": transcript,
            "phrase": request.phrase,
            "deviceId": request.deviceId
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def generate_speech_with_polly(text: str, voice_id: str = "Joanna", output_format: str = "mp3", speech_rate: str = "medium"):
    """
    Generate speech using Amazon Polly
    
    Args:
        text: Text to convert to speech
        voice_id: Polly voice ID (e.g., "Joanna", "Matthew", "Amy", "Brian")
        output_format: Output format ("mp3", "ogg_vorbis", "pcm")
        speech_rate: Speech rate ("x-slow", "slow", "medium", "fast", "x-fast")
    
    Returns:
        base64 encoded audio data
    """
    if not polly_client:
        raise HTTPException(status_code=500, detail="AWS Polly client not configured")
    
    try:
        # Add SSML for speech rate control
        ssml_text = f'<speak><prosody rate="{speech_rate}">{text}</prosody></speak>'
        
        response = polly_client.synthesize_speech(
            Text=ssml_text,
            TextType='ssml',
            OutputFormat=output_format,
            VoiceId=voice_id,
            Engine='neural'  # Use neural engine for better quality (available for most voices)
        )
        
        # Get audio stream
        audio_stream = response['AudioStream']
        audio_bytes = audio_stream.read()
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_base64
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidVoiceId':
            # Fallback to standard engine if neural is not available
            try:
                response = polly_client.synthesize_speech(
                    Text=ssml_text,
                    TextType='ssml',
                    OutputFormat=output_format,
                    VoiceId=voice_id,
                    Engine='standard'
                )
                audio_stream = response['AudioStream']
                audio_bytes = audio_stream.read()
                return base64.b64encode(audio_bytes).decode("utf-8")
            except Exception as fallback_error:
                raise HTTPException(status_code=500, detail=f"Polly TTS error: {str(fallback_error)}")
        else:
            raise HTTPException(status_code=500, detail=f"Polly TTS error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

class AnnounceBalanceRequest(BaseModel):
    userId: str
    userName: str
    includeWelcome: bool
    voiceSpeed: str
    voiceId: str = "Joanna"  # Default voice
    balance: float = 0.0  # Added actual balance field

# --- TTS Endpoint: Converts text to speech (Polly) ---
@app.post("/voice/announce-balance")
async def announce_balance(request: AnnounceBalanceRequest):
    try:
        amount_words = num2words(request.balance, lang='en')
        text = f"Hello {request.userName}, your balance is {amount_words} Naira"
        if request.includeWelcome:
            text = f"Welcome {request.userName}! " + text
        
        # Map voice speed to Polly speech rates
        speed_mapping = {
            "slow": "slow",
            "normal": "medium",
            "fast": "fast"
        }
        speech_rate = speed_mapping.get(request.voiceSpeed.lower(), "medium")
        
        audio_base64 = generate_speech_with_polly(
            text=text,
            voice_id=request.voiceId,
            speech_rate=speech_rate
        )
        
        return {"audio": audio_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Process Command
class VoiceCommandRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    sessionId: str
    context: dict

@app.post("api/voice/process-command")
async def process_command(request: VoiceCommandRequest):
    import requests
    try:
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            temp_mp3_path = temp_mp3.name

        # Now close the file before reading
        audio = AudioSegment.from_mp3(temp_mp3_path)
        result = whisper_model.transcribe(temp_mp3_path)
        transcript = result["text"]

        # Simple intent detection for demo: check for 'balance'
        if "balance" in transcript.lower():
            try:
                # For demo, userId is hardcoded as 'user123'
                resp = requests.get("http://localhost:3000/api/account/balance")
                if resp.ok:
                    data = resp.json()
                    balance = data.get("balance")
                    currency = data.get("currency", "NGN")
                    message = f"Your balance is {balance} {currency}."
                    return {
                        "status": "success",
                        "transcript": transcript,
                        "intent": "get_balance",
                        "balance": balance,
                        "currency": currency,
                        "message": message,
                        "sessionId": request.sessionId,
                        "context": request.context
                    }
                else:
                    return {
                        "status": "error",
                        "transcript": transcript,
                        "intent": "get_balance",
                        "error": "Failed to fetch balance from backend.",
                        "sessionId": request.sessionId,
                        "context": request.context
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "transcript": transcript,
                    "intent": "get_balance",
                    "error": str(e),
                    "sessionId": request.sessionId,
                    "context": request.context
                }
        # Default: just return transcript
        return {"status": "success", "transcript": transcript, "sessionId": request.sessionId, "context": request.context}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. Confirm Amount
class ConfirmAmountRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    expectedAmount: float
    spokenAmount: str

@app.post("api/voice/confirm-amount")
async def confirm_amount(request: ConfirmAmountRequest):
    try:
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            audio = AudioSegment.from_mp3(temp_mp3.name)
            temp_wav_path = temp_mp3.name.replace(".mp3", ".wav")
            audio.export(temp_wav_path, format="wav")
        result = whisper_model.transcribe(temp_wav_path)
        transcript = result["text"]
        # TODO: Compare transcript to expectedAmount/spokenAmount
        return {"status": "success", "transcript": transcript, "expectedAmount": request.expectedAmount, "spokenAmount": request.spokenAmount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 4. Capture Account
class CaptureAccountRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    accountType: str
    partialNumber: str = None
    context: str

@app.post("api/voice/capture-account")
async def capture_account(request: CaptureAccountRequest):
    try:
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            audio = AudioSegment.from_mp3(temp_mp3.name)
            temp_wav_path = temp_mp3.name.replace(".mp3", ".wav")
            audio.export(temp_wav_path, format="wav")
        result = whisper_model.transcribe(temp_wav_path)
        transcript = result["text"]
        # TODO: Parse transcript for account number
        return {"status": "success", "transcript": transcript, "accountType": request.accountType, "partialNumber": request.partialNumber, "context": request.context}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 5. Recognize Bank
class RecognizeBankRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    spokenBank: str
    context: str

@app.post("api/voice/recognize-bank")
async def recognize_bank(request: RecognizeBankRequest):
    try:
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            audio = AudioSegment.from_mp3(temp_mp3.name)
            temp_wav_path = temp_mp3.name.replace(".mp3", ".wav")
            audio.export(temp_wav_path, format="wav")
        result = whisper_model.transcribe(temp_wav_path)
        transcript = result["text"]
        # TODO: Match transcript to known banks
        return {"status": "success", "transcript": transcript, "spokenBank": request.spokenBank, "context": request.context}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 6. Verify PIN
class VerifyPinRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    transactionId: str
    sessionId: str

@app.post("api/voice/verify-pin")
async def verify_pin(request: VerifyPinRequest):
    try:
        audio_bytes = base64.b64decode(request.voiceData)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            temp_mp3.write(audio_bytes)
            temp_mp3.flush()
            audio = AudioSegment.from_mp3(temp_mp3.name)
            temp_wav_path = temp_mp3.name.replace(".mp3", ".wav")
            audio.export(temp_wav_path, format="wav")
        result = whisper_model.transcribe(temp_wav_path)
        transcript = result["text"]
        # TODO: Verify PIN from transcript
        return {"status": "success", "transcript": transcript, "transactionId": request.transactionId, "sessionId": request.sessionId}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 8. Final Confirmation
class FinalConfirmationRequest(BaseModel):
    transactionId: str
    amount: float
    recipientName: str
    recipientBank: str
    accountNumber: str
    voiceId: str = "Joanna"  # Allow voice customization

@app.post("api/voice/final-confirmation")
async def final_confirmation(request: FinalConfirmationRequest):
    try:
        text = f"Transaction {request.transactionId}: Send ${request.amount:.2f} to {request.recipientName} at {request.recipientBank}, account number {request.accountNumber}. Please confirm this transaction."
        
        audio_base64 = generate_speech_with_polly(
            text=text,
            voice_id=request.voiceId
        )
        
        return {"audio": audio_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint to get available voices
@app.get("api/voice/available-voices")
async def get_available_voices():
    """Get list of available Polly voices"""
    if not polly_client:
        raise HTTPException(status_code=500, detail="AWS Polly client not configured")
    
    try:
        response = polly_client.describe_voices(LanguageCode='en-US')
        voices = []
        for voice in response['Voices']:
            voices.append({
                'id': voice['Id'],
                'name': voice['Name'],
                'gender': voice['Gender'],
                'language': voice['LanguageName'],
                'supportedEngines': voice['SupportedEngines']
            })
        return {"voices": voices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Hardcoded demo details
HARDCODED_ACCOUNT_NUMBER = "1234567890"
HARDCODED_BANK = "GTBank"
HARDCODED_ACCOUNT_NAME = "Bola Okoro"
HARDCODED_AMOUNT = "five thousand"
HARDCODED_AMOUNT_NUM = 5000

# In-memory session state
sessions = {}

# New endpoint for welcome after login
class WelcomeRequest(BaseModel):
    userId: str
    userName: str
    voiceId: str = "Joanna"  # Default voice
    voiceSpeed: str = "medium"  # Default speed

@app.post("api/voice/welcome-after-login")
async def welcome_after_login(request: WelcomeRequest):
    try:
        # Get user balance from the backend API
        import requests
        resp = requests.get("http://localhost:3000/api/account/balance")
        balance = 0.0
        if resp.ok:
            data = resp.json()
            balance = data.get("balance", 0.0)
        
        # Format balance as words
        amount_words = num2words(balance, lang='en')
        
        # Create welcome message with options
        welcome_text = f"Welcome back {request.userName}! Your current balance is {amount_words} Naira. How may I help you today? You can say 'transfer money', 'check balance', 'purchase airtime', or 'purchase data'."
        
        # Map voice speed to Polly speech rates
        speed_mapping = {
            "slow": "slow",
            "normal": "medium",
            "fast": "fast"
        }
        speech_rate = speed_mapping.get(request.voiceSpeed.lower(), "medium")
        
        # Generate audio for welcome message
        audio_base64 = generate_speech_with_polly(
            text=welcome_text,
            voice_id=request.voiceId,
            speech_rate=speech_rate
        )
        
        # Create a new session for this user with initial state
        session_id = f"user-{request.userId}-{int(time.time())}"
        sessions[session_id] = {
            "step": "awaiting_action",
            "userId": request.userId,
            "userName": request.userName,
            "balance": balance
        }
        
        return {
            "status": "success",
            "sessionId": session_id,
            "prompt": welcome_text,
            "prompt_audio": audio_base64,
            "step": "awaiting_action"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ConverseRequest(BaseModel):
    voiceData: str  # base64-encoded mp3 audio
    sessionId: str

@app.post("api/voice/converse")
async def voice_converse(request: ConverseRequest):
    # Get or create session
    session = sessions.setdefault(request.sessionId, {"step": "welcome"})

    # Transcribe audio
    audio_bytes = base64.b64decode(request.voiceData)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
        temp_mp3.write(audio_bytes)
        temp_mp3.flush()
        temp_mp3_path = temp_mp3.name

    # Debug: copy the received mp3 to project folder for inspection
    import shutil
    try:
        shutil.copy(temp_mp3_path, "C:/Users/Hp/EmphaTech/Python_voice_service/received_debug.mp3")
        print(f"Copied received mp3 to project folder: received_debug.mp3")
    except Exception as e:
        print(f"Error copying debug mp3: {e}")

    try:
        audio = AudioSegment.from_mp3(temp_mp3_path)
    except Exception as e:
        print(f"from_mp3 failed: {e}, trying from_file with format='mp3'")
        audio = AudioSegment.from_file(temp_mp3_path, format='mp3')
    temp_wav_path = temp_mp3_path.replace(".mp3", ".wav")
    audio.export(temp_wav_path, format="wav")
    result = whisper_model.transcribe(temp_wav_path)
    transcript = result["text"].strip().lower()

    # Enhanced state machine for more natural flow
    if session["step"] == "welcome":
        if "transfer" in transcript:
            session["step"] = "awaiting_account"
            prompt = "Kindly state the account number."
        else:
            session["step"] = "awaiting_action"
            prompt = "Welcome to EmphaTech, how may I help you today? Do you want to transfer, purchase airtime, or purchase data?"
    elif session["step"] == "awaiting_action":
        if "transfer" in transcript or "send money" in transcript:
            session["step"] = "awaiting_account"
            prompt = "Kindly state the account number."
        elif "balance" in transcript or "check balance" in transcript:
            # Get user's balance if available in session
            balance = session.get("balance", 0.0)
            amount_words = num2words(balance, lang='en')
            prompt = f"Your current balance is {amount_words} Naira. Is there anything else I can help you with?"
        elif "airtime" in transcript:
            session["step"] = "awaiting_airtime_number"
            prompt = "Please provide the phone number for the airtime recharge."
        elif "data" in transcript:
            session["step"] = "awaiting_data_number"
            prompt = "Please provide the phone number for the data purchase."
        else:
            prompt = "I can help with transfers, checking balance, purchasing airtime, or purchasing data. What would you like to do?"
    elif session["step"] == "awaiting_account":
        session["step"] = "awaiting_bank"
        prompt = "Which bank?"
    elif session["step"] == "awaiting_bank":
        session["step"] = "awaiting_amount"
        prompt = f"How much would you like to send to {HARDCODED_ACCOUNT_NAME} at {HARDCODED_BANK}?"
    elif session["step"] == "awaiting_amount":
        session["step"] = "awaiting_pin"
        prompt = "Please state your four digit PIN."
    elif session["step"] == "awaiting_pin":
        # (Optionally check if transcript matches the hardcoded PIN)
        session["step"] = "awaiting_confirmation"
        prompt = f"Please confirm, you want to send {HARDCODED_AMOUNT} Naira to {HARDCODED_ACCOUNT_NAME} at {HARDCODED_BANK}, account number {HARDCODED_ACCOUNT_NUMBER}. Say 'send' to confirm."
    elif session["step"] == "awaiting_confirmation":
        if "send" in transcript:
            session["step"] = "done"
            prompt = "Transaction successful!"
        else:
            prompt = "Say 'send' to confirm the transaction."
    # Handle airtime flow
    elif session["step"] == "awaiting_airtime_number":
        session["step"] = "awaiting_airtime_amount"
        session["phone_number"] = transcript.replace(" ", "")
        prompt = "How much airtime would you like to purchase?"
    elif session["step"] == "awaiting_airtime_amount":
        session["step"] = "awaiting_airtime_pin"
        session["airtime_amount"] = transcript
        prompt = "Please state your four digit PIN."
    elif session["step"] == "awaiting_airtime_pin":
        session["step"] = "awaiting_airtime_confirmation"
        prompt = f"Please confirm, you want to purchase {session.get('airtime_amount', 'some')} Naira airtime for {session.get('phone_number', 'the number')}. Say 'confirm' to proceed."
    elif session["step"] == "awaiting_airtime_confirmation":
        if "confirm" in transcript or "yes" in transcript:
            session["step"] = "done"
            prompt = "Airtime purchase successful!"
        else:
            prompt = "Say 'confirm' to proceed with the airtime purchase."
    # Handle data flow
    elif session["step"] == "awaiting_data_number":
        session["step"] = "awaiting_data_plan"
        session["phone_number"] = transcript.replace(" ", "")
        prompt = "What data plan would you like to purchase? For example, '1GB', '2GB', or '5GB'."
    elif session["step"] == "awaiting_data_plan":
        session["step"] = "awaiting_data_pin"
        session["data_plan"] = transcript
        prompt = "Please state your four digit PIN."
    elif session["step"] == "awaiting_data_pin":
        session["step"] = "awaiting_data_confirmation"
        prompt = f"Please confirm, you want to purchase {session.get('data_plan', 'a data plan')} for {session.get('phone_number', 'the number')}. Say 'confirm' to proceed."
    elif session["step"] == "awaiting_data_confirmation":
        if "confirm" in transcript or "yes" in transcript:
            session["step"] = "done"
            prompt = "Data purchase successful!"
        else:
            prompt = "Say 'confirm' to proceed with the data purchase."
    else:
        prompt = "Thank you for using EmphaTech. Is there anything else I can help you with?"

    # Generate TTS audio for the prompt
    try:
        prompt_audio = generate_speech_with_polly(prompt)
    except Exception as e:
        prompt_audio = None

    return {
        "status": "success",
        "transcript": transcript,
        "prompt": prompt,
        "prompt_audio": prompt_audio,
        "step": session["step"]
    }