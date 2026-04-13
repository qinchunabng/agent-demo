from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime


@tool(description="获取天气，传入城市名称，返回天气描述")
def get_weather(city: str) -> str:
    return f"{city}的天气是晴天"


"""
1.agent执行前
2.agent执行后
3.model执行前
4.model执行后
5.工具执行中
6.模型执行中
"""

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent]agent启动，并附带{len(state['messages'])}个消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent]agent执行完成，共处理{len(state['messages'])}个消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before model]model开始处理消息，共{len(state['messages'])}个消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after model]model处理完成，共处理{len(state['messages'])}个消息")

@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用了")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行参数：{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，你可以根据用户的问题进行回答。",
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, tool_call_hook],
)

res = agent.invoke({
    "messages":[
        {"role": "user", "content": "明天武汉的天气如何"}
    ]
})

for message in res["messages"]:
    print(type(message).__name__, message.content)
