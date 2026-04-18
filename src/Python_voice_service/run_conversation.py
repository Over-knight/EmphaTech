import requests
import base64
import time

def audio_to_b64(filename):
    with open(filename, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

session_id = "demo-session-1"
audio_files = [
    "step1.mp3",  # "transfer"
    "step2.mp3",  # "1234567890"
    "step3.mp3",  # "GTBank"
    "step4.mp3",  # "five thousand"
    "step5.mp3",  # "one two three four" (PIN)
    "step6.mp3",  # "send"
]

for idx, audio_file in enumerate(audio_files):
    print(f"\n--- Step {idx+1} ---")
    audio_b64 = audio_to_b64(audio_file)
    print(f"Base64 length for {audio_file}: {len(audio_b64)}")
    payload = {
        "voiceData": audio_b64,
        "sessionId": session_id
    }
    response = requests.post("http://localhost:8000/voice/converse", json=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    try:
        data = response.json()
        print("Transcript:", data.get("transcript"))
        print("Prompt:", data.get("prompt"))
        # Save the TTS audio for each prompt
        if data.get("prompt_audio"):
            with open(f"prompt_{idx+1}.mp3", "wb") as f:
                f.write(base64.b64decode(data["prompt_audio"]))
            print(f"Prompt audio saved as prompt_{idx+1}.mp3")
    except Exception as e:
        print("Error decoding JSON response:", e)
    time.sleep(1)
