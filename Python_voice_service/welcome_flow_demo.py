import requests
import base64
import time
import os

# Base URL for the voice service
VOICE_SERVICE_URL = "http://localhost:8000"

# Function to play audio using system default player
def play_audio(base64_audio, output_file="welcome_audio.mp3"):
    # Decode base64 audio
    audio_bytes = base64.b64decode(base64_audio)
    
    # Save to file
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    
    # Play using system default player
    if os.name == 'nt':  # Windows
        os.system(f'start {output_file}')
    elif os.name == 'posix':  # macOS or Linux
        if os.uname().sysname == 'Darwin':  # macOS
            os.system(f'afplay {output_file}')
        else:  # Linux
            os.system(f'xdg-open {output_file}')

# Simulate user login
def simulate_login():
    print("Simulating user login...")
    # In a real app, this would be an actual login API call
    # For demo, we'll just return hardcoded user info
    return {
        "userId": "user123",
        "userName": "Empha",
        "loggedIn": True
    }

# Get welcome message after login
def get_welcome_after_login(user_info):
    print(f"Getting welcome message for user: {user_info['userName']}")
    
    # Prepare request payload
    payload = {
        "userId": user_info["userId"],
        "userName": user_info["userName"],
        "voiceId": "Joanna",  # You can change this to any available voice
        "voiceSpeed": "medium"  # Options: slow, medium, fast
    }
    
    # Make API call to welcome-after-login endpoint
    response = requests.post(f"{VOICE_SERVICE_URL}/voice/welcome-after-login", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("Welcome message received:")
        print(f"Prompt: {data.get('prompt')}")
        print(f"Session ID: {data.get('sessionId')}")
        
        # Play the welcome audio
        if data.get("prompt_audio"):
            print("Playing welcome audio...")
            play_audio(data["prompt_audio"], "welcome_audio.mp3")
        
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Simulate user voice command
def simulate_voice_command(session_id, audio_file):
    print(f"Sending voice command from file: {audio_file}")
    
    # Read audio file and convert to base64
    with open(audio_file, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Prepare request payload
    payload = {
        "voiceData": audio_base64,
        "sessionId": session_id
    }
    
    # Make API call to converse endpoint
    response = requests.post(f"{VOICE_SERVICE_URL}/voice/converse", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("Response received:")
        print(f"Transcript: {data.get('transcript')}")
        print(f"Prompt: {data.get('prompt')}")
        print(f"Step: {data.get('step')}")
        
        # Play the response audio
        if data.get("prompt_audio"):
            print("Playing response audio...")
            play_audio(data["prompt_audio"], "response_audio.mp3")
        
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Main function to demonstrate the flow
def main():
    # 1. Simulate user login
    user_info = simulate_login()
    
    if user_info["loggedIn"]:
        # 2. Get welcome message after login
        welcome_data = get_welcome_after_login(user_info)
        
        if welcome_data:
            session_id = welcome_data.get("sessionId")
            
            # Wait for user to listen to welcome message
            input("\nPress Enter after listening to the welcome message...")
            
            # 3. Demonstrate voice commands (using pre-recorded audio files)
            # You can replace these with your own audio files or record them
            audio_files = [
                "step1.mp3",  # Example: "transfer money"
                # Add more audio files as needed
            ]
            
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    response_data = simulate_voice_command(session_id, audio_file)
                    if response_data:
                        # Wait for user to listen to response
                        input("\nPress Enter after listening to the response...")
                else:
                    print(f"Audio file not found: {audio_file}")
    
    print("Demo completed!")

if __name__ == "__main__":
    main()