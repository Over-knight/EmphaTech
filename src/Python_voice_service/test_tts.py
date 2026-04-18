import requests
import base64

# Prepare the payload for the TTS endpoint
payload = {
    "userId": "user123",
    "userName": "Jude",
    "includeWelcome": True,
    "voiceSpeed": "normal",
    "voiceId": "Joanna",
    "balance": 150000.00
}

# Send the request to your FastAPI TTS endpoint
response = requests.post("http://localhost:8000/voice/announce-balance", json=payload)
data = response.json()
print(data)

# Save the returned base64 audio as an MP3 file
if "audio" in data:
    with open("tts_output.mp3", "wb") as f:
        f.write(base64.b64decode(data["audio"]))
    print("TTS audio saved as tts_output.mp3")
else:
    print("No audio returned. Error:", data)
