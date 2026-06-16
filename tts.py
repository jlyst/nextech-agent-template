# Text-to-speech example using OpenRouter's API directly with requests

import requests
import wave
import os
from dotenv import load_dotenv

load_dotenv(".env")

with open("output/script.md", "r") as f:
    script_text = f.read()

response = requests.post(
    url="https://openrouter.ai/api/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    },
    json={
        "model": "hexgrad/kokoro-82m",
        "input": script_text,
        "voice": "af_heart",
        "speed": 1.5,
    },
)
with wave.open("output/news.wav", "wb") as wf:
    wf.setnchannels(1)  # mono
    wf.setsampwidth(2)  # 16-bit = 2 bytes
    wf.setframerate(24000)  # 24 kHz
    wf.writeframes(response.content)
print(
    f"Audio saved to output/news.wav. Generation ID: {response.headers.get('X-Generation-Id')}"
)
