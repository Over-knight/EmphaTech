import base64

# Path to your MP3 file
mp3_path = "Python_voice_service/step1.mp3"
output_txt = "Python_voice_service/step1_base64.txt"

with open(mp3_path, "rb") as f:
    b64_audio = base64.b64encode(f.read()).decode("utf-8")

with open(output_txt, "w") as out:
    out.write(b64_audio)

print(f"Base64 string saved to {output_txt}")
