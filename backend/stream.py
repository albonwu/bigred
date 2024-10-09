import os
import requests
import streamlit as st
from time import time
from dotenv import load_dotenv

load_dotenv()

# Define your CSS
style = """
<style>
.stTextArea>div>div>textarea {
    font-family: "JetBrains Mono", monospace;
}
</style>
"""

# Inject CSS with markdown
st.markdown(style, unsafe_allow_html=True)

st.image("header.png")

"Convert LaTeX expressions to natural audio!"

code = st.text_area(
    "LaTeX Input:",
    placeholder="|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle",
)


def find_from_pinata_cache(tex):
    response = requests.get(
        f"https://api.pinata.cloud/v3/files?metadata[tex]={tex}",
        headers={
            "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}'
        },
    )
    response_json = response.json()
    response_files = response_json["data"]["files"]
    if response_files:
        cid = response_files[0]["cid"]
        # create signed file
        PINATA_GATEWAY = os.getenv("PINATA_GATEWAY")
        if not PINATA_GATEWAY:
            print("Error: PINATA_GATEWAY not defined environment variable")
            return
        response = requests.post(
            "https://api.pinata.cloud/v3/files/sign",
            headers={
                "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}',
            },
            json={
                "url": f"https://{PINATA_GATEWAY}/files/{cid}",
                "expires": 24 * 3600,
                "date": int(time()),
                "method": "GET",
            },
        )
        return response.json()["data"]


def handle_submit():
    signed_url = find_from_pinata_cache(code)
    if not signed_url:
        response = requests.get(
            f"http://127.0.0.1:5000/?tex={code}",
        )
        print(f"{response.text = }")
        signed_url = response.text
    st.session_state["audio_url"] = signed_url


st.button("Read!", on_click=handle_submit)

if "audio_url" in st.session_state:
    st.audio(st.session_state["audio_url"], autoplay=True)
