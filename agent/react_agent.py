from langchain.agents import create_agent

from agent.model.factory import chat_model
from agent.utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_external_data, fill_context_for_report
from agent.tools.middlware import monitor_tool, log_before_mode, report_prompt_switch


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            tools=[rag_summarize, get_weather, get_user_id, get_user_location, get_current_month, fetch_external_data, fill_context_for_report],
            system_prompt=load_system_prompt(),
            middleware=[monitor_tool, log_before_mode, report_prompt_switch],
        )

    def execute_stream(self, input: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": input}
            ]
        }
        #第三个参数context就是上下文runtime中的信息，就是提示词切换的标记
        res = self.agent.stream(input_dict, stream_mode="values", context={"report": False})
        for chunk in res:
            latest_message = chunk["messages"][-1]
            yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的地区如何保养"):
        print(chunk, end="", flush=True)

