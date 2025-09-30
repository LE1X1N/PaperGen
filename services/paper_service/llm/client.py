from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)

model = "Qwen3-4B-Instruct-2507-FP8"

def call_chat_completion(messages):
    # non-stream
    response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.8
        )
    return response.choices[0].message.content.strip()