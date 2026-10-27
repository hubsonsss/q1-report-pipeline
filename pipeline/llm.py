import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
VISION_MODEL = "openai/gpt-4o-mini"
TEXT_MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

client = OpenAI(base_url=BASE_URL, api_key=os.getenv("OPENROUTER_API_KEY"))


def chat(prompt: str, system: str = "You are a helpful analyst.") -> str:
    resp = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content


def describe_image(path: str, prompt: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    resp = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data}"}},
                ],
            }
        ],
    )
    return resp.choices[0].message.content
