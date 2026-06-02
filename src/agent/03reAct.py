from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="获取体重，返回值是整数，单位是千克")
def get_weight() -> int:
    return 75

@tool(description="获取身高，返回值是整数，单位是厘米")
def get_height() -> int:
    return 180


agent = create_agent(
    model=ChatOllama(model="qwen3.5:9b",base_url="http://localhost:11434"),
    tools=[get_weight,get_height],
    system_prompt="你是严格遵守ReAct框架的智能体，必须按照【思考→行动→观察→在思考】的流程解决问题，"
    "每轮仅能思考并调用一个工具，禁止单词调用多个工具，"
    "并把思考过程告诉用户，为什么调用某个工具等。按照思考，行动，观察三个结构告知我"
)
for chunk in agent.stream(
    {
        "messages":[
            {"role": "user", "content": "计算我的BMI"},
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