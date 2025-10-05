import os
from openai import OpenAI

from src.config import conf


client = OpenAI(
    base_url=conf["openai"]["base_url"],
    api_key=os.getenv("OPENAI_API_KEY")
)

def call_chat_completion(messages):
    # non-stream
    response = client.chat.completions.create(
            messages=messages,
            model=conf["openai"]["model"],
            temperature=0.8
        )
    return response.choices[0].message.content.strip()