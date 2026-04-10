from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取天气")
def get_weather() -> str:
    return "晴天"

agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，你可以根据用户的问题进行回答。",
)

res = agent.invoke({
    "messages":[
        {"role": "user", "content": "明天武汉的天气如何"}
    ]
})

for message in res["messages"]:
    print(type(message).__name__, message.content)
