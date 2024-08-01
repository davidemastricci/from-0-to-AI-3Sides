import base64
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found in .env file")


# Function to encode the image
def _encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# Function to extract content from the response
def _extract_content(response_json):
    try:
        return response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError("Content not found in the response") from e


# Method to process the image and return content
def process_image(image):
    base64_image = _encode_image(image)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Act as a social media manager having an experience of 12 years in the industry. \
                        Your job is to create calls to action that gain more followers, engagement, conversions, particularly \
                        saves and shares based on the image. My Niche is crafted streetweare and my goal is \
                        to describe the picture.Tone of voice is to speak with \
                        teenagers and young adults.Write the caption in Italian",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    response_json = response.json()

    try:
        content = _extract_content(response_json)
        return content
    except ValueError as e:
        return str(e)


# Example usage
# image_path = "/Users/davidemastricci/Documents/personal_workspace/from-0-to-AI-3Sides/data_sample/goodexaple2.jpg"
# image = Image.open(image_path)
# content = process_image(image)
# print("Extracted content:")
# print(content)
