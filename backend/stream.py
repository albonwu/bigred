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
    requests.get(
        f"http://127.0.0.1:5000/?tex={code}",
    )


st.button("Submit", on_click=handle_submit)
