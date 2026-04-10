from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取股票价格，传入股票名称，返回字符串信息")
def get_price(name: str) -> str:
    return f"股票{name}的价格是100元"

@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name: str) -> str:
    return f"{name}是一家A股上市公司，专注于IT职业教育"

agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_price,get_info],
    system_prompt="你是一个专业的股票助手，你可以根据用户的问题进行回答。请告诉我思考过程，让我知道你为什么调用某个工具",
)

res = agent.stream(
    {"messages":[{"role":"user","content":"传智教育的股价多少，并介绍一下公司"}]},
    stream_mode="values",
)

for chunk in res:
    message = chunk["messages"][-1]
    if message.content:
        print(type(message).__name__, message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print(f"工具调用：{ [call['name'] for call in message.tool_calls] }")
