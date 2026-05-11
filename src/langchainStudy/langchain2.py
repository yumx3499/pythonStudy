#longchain 对大语言模型的访问
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen2.5:7b",base_url="http://localhost:11434")

response = model.invoke(input="请用python代码实现一个冒泡排序算法")
print(response)

res_stream = model.stream(input="请用python代码实现一个经典列表遍历算法")

for chunk in res_stream:
    print(chunk,end="",flush=True)
