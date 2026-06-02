from langchain_core.prompts import ChatPromptTemplate
import config.config_data as config
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from vector_stores import VectorStoryService
from langchain_core.runnables import RunnablePassthrough,RunnableWithMessageHistory,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.prompts import MessagesPlaceholder
from history_stores import FileChatMessageHistory


class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoryService(
            OllamaEmbeddings(model=config.embedding_model,base_url="http://localhost:11434")
            )

        self.prompt = ChatPromptTemplate.from_messages(
                [("system", "你是一个公司的助手，请完全根据提供的资料回答用户的提问，资料以外的内容请忽略。"
                    "并附带所有相关的元数据。"
                  "如果没找到答案，请不要瞎编回答，回复：未找到相关内容。提供的资料{context}"),
                  ("system", "并且我会提供历史会话记录.记录如下："),
                MessagesPlaceholder("chat_history"),
                ("user", "{input}")
                ]
            )

        self.chat_model=OllamaLLM(model=config.chat_model,base_url="http://localhost:11434")

        self.session_config = {
            "configurable": {
                "session_id": "user001"}
        }
        self.chain = self.__get_chain()

    def prompt_format(self ,docs: list[Document]):
        if not docs:
            return ""
        format_str =""
        for doc in docs:
            format_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n"
        return format_str

    def get_sessionid(self,sessionid):
        return FileChatMessageHistory(sessionid)
    def prompt_print(self,prompt):
        print("#"*50+"调试信息" +"#"*50)
        print(prompt)
        print("#"*50+"调试信息" +"#"*50)
        print(type(prompt))
        print("#"*50+"调试信息" +"#"*50)
        return prompt
    def input_format1(self,value: dict):
        new_input = value["input"]
        return new_input
    def input_format2(self,value: dict):
        new_input = {}
        new_input["input"] = value["input"]["input"]
        new_input["context"] = value["context"]
        new_input["chat_history"] = value["input"]["chat_history"]
        return new_input
    def __get_chain(self):
        retriever = self.vector_store.get_retriever()
        base_chain = {
            "input": RunnablePassthrough(),
            "context": RunnableLambda(self.input_format1) 
            | retriever 
            | self.prompt_format

        } | RunnableLambda(self.input_format2)| RunnableLambda(self.prompt_print) |self.prompt |  self.chat_model | StrOutputParser()

        chain = RunnableWithMessageHistory(
            base_chain,
            self.get_sessionid,
            input_messages_key="input",
            history_messages_key="chat_history"
        ) 

        return chain
    def get_answer(self,question):
        return self.chain.stream({"input":question},config=self.session_config)

if __name__ == '__main__':
    res = RagService().get_answer("请给我关于退货率的分析")
    print(res)