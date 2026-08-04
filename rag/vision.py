import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_code_image(image_bytes, mime_type, question):
    """
    Analyze a programming-related image such as:
    - Code screenshot
    - IDE screenshot
    - Terminal error
    - Flowchart
    - UML diagram
    """

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=[
            {
                "text":
                f"""
                You are an expert programming assistant.

                Analyze the uploaded programming image.

                The image may contain:

                • Source Code
                • IDE Screenshot
                • Terminal Output
                • Compiler Errors
                • Flowcharts
                • UML Diagrams

                User Question:

                {question}

                Give a detailed explanation.
                """
            },
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_bytes
                }
            }
        ]
    )

    return response.text