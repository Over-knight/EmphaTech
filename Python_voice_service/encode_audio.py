import base64

# Change 'myvoice.mp3' to your audio file's name
with open("sendmoney.mp3", "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

print(audio_base64)
