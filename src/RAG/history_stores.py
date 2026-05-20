from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage,messages_from_dict,message_to_dict
from typing import Sequence
import os,json
import config.config_data as config

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.storage_path = config.history_storage_path
        self.session_id = session_id
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                os.path.join(self.storage_path, self.session_id),
                "r",
                encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        messages_data = [message_to_dict(message) for message in messages]
        with open(
            os.path.join(self.storage_path, self.session_id),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(messages_data, f)
    def clear(self) -> None:
        with open(
            os.path.join(self.storage_path, self.session_id),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump([], f)