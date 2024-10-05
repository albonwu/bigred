import os
import subprocess
import time
from flask import Flask, Response, request
from flask_cors import CORS
from dotenv import load_dotenv
from cartesia import Cartesia
import requests
from datetime import datetime

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
    tex = request.args.get("tex")
    print(f"{tex = }")
    transcript = tex or "E equals M C squared"

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

    response = requests.post(
        "https://uploads.pinata.cloud/v3/files",
        headers={
            "authorization": f"Bearer {os.environ.get('PINATA_API_JWT')}",
        },
        files={
            "file": (
                f"{datetime.today().isoformat()}.wav",
                open("temp.wav", "rb"),
                "audio/x-wav",
            )
        },
    )
    if not response.ok:
        print("error in uploading file!")
        print(f"{response.text = }")
        return "error in uploading file!", 500
    res_data = response.json()["data"]
    id = res_data["id"]
    cid = res_data["cid"]
    response = requests.put(
        f"https://api.pinata.cloud/v3/files/{id}",
        headers={
            "authorization": f"Bearer {os.environ.get('PINATA_API_JWT')}",
        },
        json={
            "keyvalues": {"tex": tex},
        },
    )
    if not response.ok:
        print("error while updating file metadata")
        print(f"{response.text = }")
        return "error while updating file metadata!", 500
    response = requests.post(
        f"https://api.pinata.cloud/v3/files/sign",
        headers={
            "authorization": f"Bearer {os.environ.get('PINATA_API_JWT')}",
        },
        json={
            "url": f"https://{os.environ.get('PINATA_GATEWAY')}/files/{cid}",
            "date": int(time.time()),
            "expires": 24 * 3600,
            "method": "GET",
        },
    )
    if not response.ok:
        print("error while getting signed url!")
        print(f"{response.text = }")
        return "error getting signed url!", 500
    signed_url = response.json()["data"]
    return signed_url


@app.route("/test")
def test():
    pass
