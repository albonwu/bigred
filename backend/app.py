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

    with open("temp.pcm", "wb") as f:
        for audio_chunk in client.tts.sse(
            model_id=model_id,
            transcript=transcript,
            voice_embedding=voice["embedding"],
            output_format=output_format,
            stream=True,
        ):
            f.write(audio_chunk["audio"])

    subprocess.run("ffmpeg -y -f f32le -i temp.pcm temp.wav", shell=True)

    return "fuck"


@app.route("/test")
def test():
    response = requests.post(
        "https://uploads.pinata.cloud/v3/files",
        headers={
            "authorization": f"Bearer {os.environ.get('PINATA_API_JWT')}",
        },
        files={"file": ("yippee.wav", open("temp.wav", "rb"), "audio/x-wav")},
    )
    return response.text
