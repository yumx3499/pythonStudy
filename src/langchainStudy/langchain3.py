# langchain 中聊天模型的调用
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

model = ChatOllama(model="qwen2.5:7b",base_url="http://localhost:11434")

messages = [
    SystemMessage(content="你是一个边塞诗人，请用古风的语言描述一下元月的景色"),
    HumanMessage(content="请用古风的语言描述一下元月的景色"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="请先把上一次的回复告诉我，然后请根据上面的诗句，写一首同字数格式的诗歌"),


]
res = model.invoke(input=messages)

print(res.content)

res_stream = model.stream(input=messages)
for chunk in res_stream:
    print(chunk.content, end="", flush=True)