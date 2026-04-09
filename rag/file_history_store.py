import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import messages_from_dict, BaseMessage, messages_to_dict

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

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