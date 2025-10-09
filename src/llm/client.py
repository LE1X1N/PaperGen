import os
from openai import AsyncOpenAI
import asyncio

from src.config import conf


client = AsyncOpenAI(
    base_url=conf["openai"]["base_url"],
    api_key=os.getenv("OPENAI_API_KEY")
)

async def call_chat_completion_async(messages: list) -> str:
    # non-stream
    response = await client.chat.completions.create(
            messages=messages,
            model=conf["openai"]["model"],
            temperature=0.8
        )
    return response.choices[0].message.content.strip()

def call_chat_completion(messages: list) -> str:
    return asyncio.run(call_chat_completion_async(messages))