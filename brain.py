import os
from groq import Groq
import base64

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# image_path ="ronaldo.jpg"
def encode_image(image):
    if isinstance(image, (str, os.PathLike)):
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    else:  # assume file-like object (e.g., BytesIO)
        return base64.b64encode(image.read()).decode("utf-8")

query="Brief me on football player?"
model ="meta-llama/llama-4-maverick-17b-128e-instruct"

def analyse_image_with_query(query, model, encoded_image):
    client = Groq()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    }
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
