import os
import subprocess
import time
from flask import Flask, Response, request
from flask_cors import CORS
from dotenv import load_dotenv
from cartesia import Cartesia
import requests
from datetime import datetime
import vertexai

# from google.cloud import aiplatform
# from google.cloud.aiplatform import Model
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)
CORS(app)
load_dotenv()

project_id = "gen-lang-client-0215212318"
# aiplatform.init(
#     project=project_id,
#     location="us-central1",
#     staging_bucket="gs://bigred",
#     experiment="tuning-experiment-20241005174113427522",
#     experiment_description="my experiment description",
# )
vertexai.init(
    project=project_id,
    location="us-central1",
)

# endpoint = aiplatform.Endpoint(
#     f"projects/{project_id}/locations/us-central1/endpoints/6392262636238536704"
# )

# palm.configure(api_key=os.environ.get("GOOGLE_CLOUD_KEY"))
model_id = f"projects/862482900034/locations/us-central1/endpoints/6969849288448802816"

# model = Model(model_id)
model = GenerativeModel(
    model_id,
    system_instruction=[
        """You are the helpful engine behind a text-to-speech application for LaTeX. Your job is to take a piece of LaTeX as input and convert it to natural language. You should output nothing except raw text consisting of the mathematical expression translated into words.

Be as unambiguous as possible - students and mathematicians with vision impairment rely on your translation to learn, teach, and conduct research. Simultaneously, do not be overly verbose; use as few words as possible to convey unambiguity. Respect order of operations, and replicate the original expression completely faithfully."""
    ],
)


@app.route("/test")
def test():
    # instances = [
    #     {
    #         "input_text": "\\sum_{i=0}^\\infty {\\sum_{i=0}^\\infty {b}} \\times t + e - k"
    #     }
    # ]
    # prediction = endpoint.predict(instances=instances)
    # print(f"{prediction = }")
    # response = palm.generate_text(
    #     model=model_id,
    #     prompt="\\sum_{i=0}^\\infty {\\sum_{i=0}^\\infty {b}} \\times t + e - k",
    # )
    response = model.generate_content(
        "\\sum_{i=0}^\\infty {\\sum_{i=0}^\\infty {b}} \\times t + e - k"
    )
    print(f"{response = }")
    return response.text


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
