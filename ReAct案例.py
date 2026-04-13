from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取体重，返回值是整数，单位是千克")
def get_weight() -> int:
    return 70

@tool(description="获取身高，返回值是整数，单位是厘米")
def get_height():
    return 170


agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_height, get_weight],
    system_prompt="""
    你是严格遵守ReAct框架的的智能体，必须按照[思考->行动->观察->再思考]的流程解决问题，
    且**每轮仅能思考并调用一个工具**，禁止单次调用多个工具。
    并告知你思考的过程，工具调用的原因，按照思考、行动、观察三个结构告知我。
    """,
)

res = agent.stream(
    {"messages":[{"role":"user","content":"计算我的BMI"}]},
    stream_mode="values",
)

for chunk in res:
    message = chunk["messages"][-1]
    if message.content:
        print(type(message).__name__, message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print(f"工具调用：{ [call['name'] for call in message.tool_calls] }")
