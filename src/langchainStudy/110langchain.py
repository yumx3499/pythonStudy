# 110-langchain
# chain

from langchain_ollama import ChatOlama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
import os
import json
from typing import Sequence


prompt = ChatPromptTemplate.from_template("你是一个资深后端开发工程师，请根据下面的需求，生成技术方案: {input}")
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个资深后端开发工程师"),
#     ("user", "{input}")
# ])

# 直接调用模型
model = ChatOlama(model="qwen2.5:7b",base_url="http://localhost:11434")

# 输出解析器
str_output_parser = StrOutputParser()


class FileChatMessageHistory(BaseChatMessageHistory):
    storage_path: str
    session_id: str

    def __init__(self, storage_path: str, session_id: str):
        self.storage_path = storage_path
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
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages
        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

FileChatMessageHistory()


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深后端开发工程师"),
    ("user", "{input}")
])

# 创建一个 chain
chain = prompt | model | str_output_parser


# 调用 chain
result = chain.invoke({"input": "我想做一个用户管理系统，支持注册、登录、用户信息修改和查询，用户表设计、接口设计、鉴权方案，只返回核心内容，不要废话"})
print(result)
