import os

from openai import OpenAI


client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("AI_DASHSCOPE_API_KEY"),
)

response = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {"role": "system", "content": "你是AI助理，你回答用户的问题很简洁"},
        {"role": "user", "content": "小明有2条宠物狗"},
        {"role":"assistant", "content": "好的"},
        {"role":"user", "content": "小红有3个宠物猫咪"},
        {"role":"assistant", "content": "好的"},
        {"role":"user", "content": "总共有几个宠物?"},
    ],
    # extra_body={"enable_thinking": True},
    stream=True
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in response:
    if chunk.choices[0].delta.reasoning_content is not None:
        print(chunk.choices[0].delta.reasoning_content, end=" ", flush=True)