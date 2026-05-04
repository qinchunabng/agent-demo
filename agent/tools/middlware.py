from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command

from agent.utils.logger_handler import logger
from agent.utils.prompt_loader import load_report_prompt, load_system_prompt


@wrap_tool_call
def monitor_tool(request: ToolCallRequest,
                 handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    """
    监控工具调用
    :return:
    """
    logger.info(f"[tool_monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool_monitor]工具调用参数：{request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool_monitor]工具{request.tool_call['name']}调用结果：{result}")

        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report'] = True
        return result
    except Exception as e:
        logger.error(f"[tool_monitor]工具调用失败：{e}")
        raise e

@before_model
def log_before_mode(state: AgentState,
                    runtime: Runtime):
    logger.info(f"[log_before_mode]即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_mode]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt   #每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get('report', False)
    if is_report:
        return load_report_prompt()
    return load_system_prompt()

