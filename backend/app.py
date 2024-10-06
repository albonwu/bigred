import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from cartesia import Cartesia

app = Flask(__name__)
CORS(app)
load_dotenv()

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def index():
    data = request.get_json()
    print(f"{data = }")
    text = "E equals M C squared"

    return "yippee!"
