import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part


def multiturn_generate_content():
    vertexai.init(project="862482900034", location="us-central1")
    model = GenerativeModel(
        "projects/862482900034/locations/us-central1/endpoints/6969849288448802816",
        system_instruction=[textsi_1]
    )
    chat = model.start_chat()
    print(chat.send_message(
        ["""C = \\sqrt[3]{\\frac{\\Delta_{1} \\pm \\sqrt{\\Delta_{1}^{2} - 4\\Delta_{0}^{3}}}{2}}"""],
        generation_config=generation_config,
        safety_settings=safety_settings
    ))

textsi_1 = """You are the helpful engine behind a text-to-speech application for LaTeX. Your job is to take a piece of LaTeX as input and convert it to natural language. You should output nothing except raw text consisting of the mathematical expression translated into words.

Be as unambiguous as possible - students and mathematicians with vision impairment rely on your translation to learn, teach, and conduct research. Simultaneously, do not be overly verbose; use as few words as possible to convey unambiguity. Respect order of operations, and replicate the original expression completely faithfully."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.2,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

multiturn_generate_content()
