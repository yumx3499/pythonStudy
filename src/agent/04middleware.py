from langchain.agents import create_agent,AgentState
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents.middleware import before_agent,after_agent,before_model,after_model,wrap_model_call,wrap_tool_call
from langgraph.runtime import Runtime
from datetime import datetime
import src.RAG.config.config_data as config
@tool(description="查询时间，返回时间信息")
def get_time():
    return datetime.now()
@tool(description="查询城市天气，传入城市名称，返回天气信息")
def get_weather_city(city: str):
    return f"{city}今天是晴天"
@tool(description="查询北京天气")
def get_weather_beijing():
    return "今天多云转晴。"
@before_agent
def log_before_agent(state:AgentState,runtiem:Runtime) -> None:
    print(f"[befor agent]agent启动，并附带{len(state['messages'])}条消息。")
          
@after_agent
def log_after_agent(state:AgentState,runtiem:Runtime) -> None:
    print(f"[after agent]agent结束，并附带{len(state['messages'])}条消息。")
          

@before_model
def log_before_model(state:AgentState,runtiem:Runtime) -> None:
    print(f"[befor model]model启动，并附带{len(state['messages'])}条消息。")
          
@after_model
def log_after_model(state:AgentState,runtiem:Runtime) -> None:
    print(f"[after model]model结束，并附带{len(state['messages'])}条消息。")

@wrap_model_call
def model_call_hook(request,handler):
    print("model调用le")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"tool执行：{request.tool_call['name']}")
    print(f"tool执行参数：{request.tool_call['args']}")
    return handler(request)


agent = create_agent(
    model=ChatOllama(model=config.chat_model,base_url="http://localhost:11434"),
    tools=[get_time,get_weather_city,get_weather_beijing],
    middleware=[log_before_agent,log_after_agent,log_before_model,log_after_model,model_call_hook,monitor_tool],
    system_prompt="你是一个聊天助手，请根据用户输入内容进行回答。"
    
)
for chunk in agent.stream(
    {
        "messages":[
            {"role": "user", "content": "现在几点了"},
        ]

    },
    stream_mode="values"
):
    last_chunk = chunk['messages'][-1]
    if last_chunk.content:
        print(type(last_chunk.content).__name__,last_chunk.content)
    
    try:
        if last_chunk.tool_calls:
            for tool_call in last_chunk.tool_calls:
                print(type(tool_call['name']).__name__,tool_call['name'])
                print(type(tool_call['args']).__name__,tool_call['args'])
    except AttributeError as e:
        pass