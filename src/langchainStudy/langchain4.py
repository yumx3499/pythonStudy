# langchain 中聊天模型的简写格式

from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5:7b",base_url="http://localhost:11434")

messages = [
    ("system","你是一个英语老师，请用英语描述一下元月的景色"),
    ("human","请用英语一句话描述一下元月的景色,并附上翻译"),
    ("ai","The scenery of the first month is beautiful."),
    ("human","请用英文描述一下元月的景色,并附上翻译"),
]

# res = model.invoke(input=messages)
# print(res.content)

res_stream = model.stream(input=messages)
for chunk in res_stream:
    print(chunk.content, end="", flush=True)