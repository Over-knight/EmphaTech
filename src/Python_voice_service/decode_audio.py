import base64

# Read your base64 string from the file
with open("audio_b64.txt", "r") as f:
    audio_base64 = f.read().replace('\n', '')

# Decode and save as MP3
with open("step1.mp3", "wb") as f:
    f.write(base64.b64decode(audio_base64))

print("Decoded audio saved as decoded_test.mp3")
