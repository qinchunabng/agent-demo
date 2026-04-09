from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(
    model='qwen3-max'
)

prompt = PromptTemplate.from_template(
    "你需要根据历史会话内容，回答用户的问题。历史会话内容：{history}，用户问题：{input}"
)

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print('='*20, full_prompt.to_string(), '='*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

store = {}
def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key='input',
    history_messages_key='history',
)



if __name__ == '__main__':

    session_config = RunnableConfig(configurable={
        'session_id': '123',
    })

    res = conversation_chain.invoke({"input": "小明有两个猫"}, config=session_config)
    print("第一次调用:",res)

    res = conversation_chain.invoke({"input": "小刚有一只狗"}, config=session_config)
    print("第二次调用:",res)

    res = conversation_chain.invoke({"input": "总共有几只宠物"}, config=session_config)
    print("第三次调用:",res)