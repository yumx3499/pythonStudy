from langchain_core.prompts import ChatPromptTemplate ,MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

promptTemplate = ChatPromptTemplate.from_messages([
    ("system","你是一个{role}老师，请根据学生输入的{word}单词，做一小段文章。"),
    MessagesPlaceholder("chat_history"),
    ("user","{input}")
])

strout = StrOutputParser()
def print_prompt(prompt):
    print("="*10+ prompt.to_string()+"="*10)
    return prompt

session_store ={}  
def get_sessionid(sessionid):
    if sessionid not in session_store:
        session_store[sessionid] = InMemoryChatMessageHistory()
    return session_store[sessionid]


model = ChatOllama(model="qwen2.5:7b",base_url="http://localhost:11434")

base_chain = promptTemplate | print_prompt | model | strout


conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_sessionid,
    input_messages_key="input",
    history_messages_key="chat_history"
)

session_config ={
    "configurable":{
        "session_id":"user1"
    }
}

resp = conversation_chain.stream({"role":"英语","word":"english",
                   "input":"apple"},
                   session_config)
for chunk in resp:    
    print(chunk, end="", flush=True)