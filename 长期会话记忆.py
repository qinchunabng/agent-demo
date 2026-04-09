import json
import os.path
from typing import Sequence

import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id, store_path):
        self.session_id = session_id
        self.store_path = store_path

        self.file_path = os.path.join(self.store_path, self.session_id)
        self._messages = []
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._load_messages()


    def _load_messages(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_data = json.load(f)
                self._messages = messages_from_dict(messages_data) if messages_data else []
        except (FileNotFoundError, json.JSONDecodeError):
            self._messages = []


    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        self._messages.extend(messages)
        
        all_messages_dict = messages_to_dict(self._messages)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(all_messages_dict, f, ensure_ascii=False, indent=2)

    @property
    def messages(self) -> list[BaseMessage]:
        return self._messages

    def clear(self) -> None:
        self._messages = []
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


model = ChatTongyi(
    model='qwen3-max'
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回应用户问题。对话历史："),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
   ])

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print('='*20, full_prompt.to_string(), '='*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key='input',
    history_messages_key='chat_history',
)

if __name__ == '__main__':
    session_config = {
        "configurable": {
            "session_id": "123",
        }
    }

    # res = conversation_chain.invoke({"input": "小明有两个猫"}, config=session_config)
    # print("第一次调用:", res)
    #
    # res = conversation_chain.invoke({"input": "小刚有一只狗"}, config=session_config)
    # print("第二次调用:", res)

    res = conversation_chain.invoke({"input": "总共有几只宠物"}, config=session_config)
    print("第三次调用:", res)