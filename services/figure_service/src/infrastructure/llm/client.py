import os
from openai import OpenAI

from src.errors import OpenAIError
from src.config import conf

 # OpenAI client
client = OpenAI(
    base_url=conf["openai"]["base_url"],
    api_key=os.getenv("OPENAI_API_KEY")
)

def call_chat_completion(messages, **kwargs):
    """
        Call LLM to generate code
    """
    try:
        # openai compatible
        response = client.chat.completions.create(
                model=conf["openai"]["model"],  
                messages=messages,
                stream=True,
                **kwargs
            )
        
        full_content = []
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                full_content.append(chunk.choices[0].delta.content) 
        return ''.join(full_content)
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise OpenAIError(f"OpenAI 接口调用失败: {error_msg}") from e
    

def check_openai_health():
    messages=[{"role": "user", "content": "ping"}]
    try:
        call_chat_completion(messages, max_completion_tokens=5)
        print(f"OpenAI 检查通过！默认模型：{conf["openai"]["model"]}")
    except OpenAIError:
        raise
    