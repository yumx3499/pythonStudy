from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

prompt = PromptTemplate.from_template("这是我的模板试验，刚刚使用了{template_var},请告诉我{prompt_var}有什么需要注意的问题？")

model = OllamaLLM(model="qwen2.5:7b",base_url="http://localhost:11434")

chain = prompt | model
res = chain.invoke({"template_var": "PromptTemplate", "prompt_var": "为什么要使用模板？"}) 
print(res)