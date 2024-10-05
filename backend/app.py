import os
import subprocess
from flask import Flask, Response, request
from flask_cors import CORS
from dotenv import load_dotenv
from cartesia import Cartesia
import requests

app = Flask(__name__)
CORS(app)
load_dotenv()

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
model_id = "sonic-english"
voices = client.voices.list()
voice = None
for voice_data in voices:
    if voice_data["name"] == "Anime Girl":
        print(f'{voice_data["id"] = }')
        voice = voice_data
        break
else:
    print("failed to find voice_id!")
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}


@app.route("/")
def index():
    data = request.args.get("tex")
    print(f"{data = }")
    transcript = data or "E equals M C squared"

    response = requests.post(
        "https://api.cartesia.ai/tts/bytes",
        headers={
            "Cartesia-Version": "2024-10-05",
            "X-API-Key": os.environ.get("CARTESIA_API_KEY"),
            "Content-Type": "application/json",
        },
        json={
            "transcript": transcript,
            "model_id": model_id,
            "voice": {
                "mode": "id",
                "id": "1001d611-b1a8-46bd-a5ca-551b23505334",
            },
            "output_format": output_format,
        },
    )

    with open("temp.pcm", "wb") as f:
        f.write(response.content)
    subprocess.run("ffmpeg -f -y f32le -i temp.pcm temp.wav", shell=True)

    return "fuck"
