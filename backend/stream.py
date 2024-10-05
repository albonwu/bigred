import requests
import streamlit as st

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

code = st.text_area(
    "LaTeX Input",
    placeholder="|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle",
)


def handle_submit():
    requests.post(
        # "https://webhook.site/2022a60b-2d8a-4a0a-b009-c01682a0b0e3",
        "http://127.0.0.1:5000/",
        json={"code": code},
    )


st.button("Submit", on_click=handle_submit)
