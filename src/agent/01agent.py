from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
@tool(description="查询大连天气")
def get_weather_dalian():
    return "今天天是晴天"
@tool(description="查询北京天气")
def get_weather_beijing():
    return "今天多云转晴。"


agent = create_agent(
    model=ChatOllama(model="qwen3.5:9b",base_url="http://localhost:11434"),
    tools=[get_weather_dalian,get_weather_beijing],
    system_prompt="你是一个聊天助手，请根据用户输入内容进行回答。"
    
)
res = agent.invoke(
    {
        "messages":[
            {"role": "user", "content": "北京今天天气如何？"},
        ]

    }
)
for msg in res["messages"]:
    print(type(msg).__name__,msg.content)