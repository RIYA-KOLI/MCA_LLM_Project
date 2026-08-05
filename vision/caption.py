import os
import ollama

MODEL_NAME = "qwen2.5vl:3b"


def analyze_image(image_source):
    """
    Generate a caption for an image using Qwen2.5-VL.

    Parameters:
        image_source (str): Path to the image.

    Returns:
        str: AI-generated image caption.
    """

    # Verify the file exists
    if not os.path.exists(image_source):
        return f"⚠️ Image not found:\n\n{image_source}"

    try:

        response = ollama.chat(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",

                    "content": """
You are Vision AI for a Programming Help Assistant.

Analyze the uploaded image.

If it is:

• A normal photograph:
Describe it in detail.

• A programming screenshot:
Explain what is visible.

• Source code:
Summarize the code.

• A compiler or runtime error:
Explain the error.

• A flowchart or UML diagram:
Explain what it represents.

• A handwritten note:
Read the visible text if possible.

Provide a clear and structured response.
""",

                    "images": [image_source],
                }
            ],

            keep_alive=-1,

            options={
                "temperature": 0.2,
            }

        )

        return response["message"]["content"]

    except Exception as e:

        return f"⚠️ Vision Error:\n\n{e}"