from langchain_core.prompts import ChatPromptTemplate ,MessagesPlaceholder
from langchain_ollama import ChatOllama

promptTemplate = ChatPromptTemplate.from_messages([
    ("system", "你是一个语文老师，请根据学生输入的单词，做一小段文章。"),
    MessagesPlaceholder("history"),
    ("user", "{input}")
])

history_date = [
    ("user","你来做一个关于“苹果”的文章"),
    ("ai", "在秋日里，有一样水果总是让人垂涎欲滴——那就是苹果。它不仅是人们喜爱的一种水果，而且也是我们生活中的常见食品之一。")
]

prompt_text = promptTemplate.invoke({"input": "先告诉我，我上一个问题的内容和你上一个回复，要原文，然后请写一个关于“香蕉”的文章。", "history": history_date})

model = ChatOllama(model="qwen2.5:7b",base_url="http://localhost:11434")

res = model.invoke(prompt_text)

print(res.content)