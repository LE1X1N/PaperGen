from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)


system_prompt = "You are a helpful scientic paper writer."
model = "Qwen3-4B-Instruct-2507-FP8"
thesis_name = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"

if __name__ == "__main__":

    response = client.chat.completions.create(
        messages=[
            {'role':'assistant', 'content': system_prompt},
            {'role': 'user', 'content': f'Write a thsis structure for <{thesis_name}>'}
        ],
        model=model
    )
    
    print(response.choices[0].message.content)
