from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    data = request.get_json()
    print(f"{data = }")
    text = "E equals M C squared"

    return "yippee!"
