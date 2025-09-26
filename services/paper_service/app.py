from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)


if __name__ == "__main__":

    response = client.chat.completions.create(
        messages=[
            {'role':'assistant', 'content': "You are a helpful scientic paper writer."},
            {'role': 'user', 'content': 'Write a thsis structure for <基于Android+XAMPP+MySQL的家校互动平台设计与实现>'}
        ],
        model="Qwen3-4B-Instruct-2507-FP8"
    )
    
    print(response.choices[0].message.content)
