from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="获取股票价格，需要传入股票名称")
def get_stock_price(stock_name: str) -> str:
    return f"{str}股票价格是：100"

@tool(description="获取股票信息，需要传入股票名称")
def get_stock_info(stock_name: str) -> str:
    return f"{str}是一家A股上市公司，公司主要业务是提供网络服务，目前有300家分公司分布全国各地。"


agent = create_agent(
    model=ChatOllama(model="qwen3.5:4b",base_url="http://localhost:11434"),
    tools=[get_stock_price,get_stock_info],
    system_prompt="你是一个智能助手，你需要根据用户输入回答问题，并把思考过程告诉用户，为什么调用某个工具等。"
)
for chunk in agent.stream(
    {
        "messages":[
            {"role": "user", "content": "鑫秀科技公司介绍，并且股价是多少？"},
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