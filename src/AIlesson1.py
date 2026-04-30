from openai import OpenAI 

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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"
# )

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

def model_input(input_text):
    # while True:
        question = input_text
        # if question == 'q':
        #     q = input("确定要退出吗？y/n：")
        #     if q == "y":
        #         break
        #     else: 
        #         continue
        # if question == '':
        #     continue
        response = client.chat.completions.create(
            model="tencent/hy3-preview:free",
            messages=[
                {"role":"system","content":"你是一个python编程的专家，可以很简单明了的把我不会的概念教授给我"},
                {"role":"user","content":question}
            ]
        )

        return response.choices[0].message.content
def model_input_streaming(input_text):
    # while True:
        question = input_text
        input_len = len(input_text)
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=[
                {"role":"system","content":"你是一个python编程的专家，可以很简单明了的把我不会的概念教授给我"},
                {"role":"user","content":question}
            ],
            stream=True
        )
        # 统计变量
        total_tokens = 0
        chunk_count = 0
        
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content: 
                total_tokens += len(content)  # 简单估算 token 数
                chunk_count += 1
                yield content
        
        # 打印本次请求统计
        print(f"[统计] input:{input_len},chunks: {chunk_count}, 估算字符数: {total_tokens}")



def main2():

    messages =[{"role":"system","content":"你是一个python编程的专家，可以很简单明了的把我不会的概念教授给我"}]
    while True:
        question = input("用户：")
        if question == 'q':
            q = input("确定要退出吗？y/n：")
            if q == "y":
                break
            else: 
                continue
        if question == '':
            continue
        messages.append({"role":"user","content":question})
        response = client.chat.completions.create(
            model="tencent/hy3-preview:free",
            messages=messages,
            stream=True
        )
        msg=""
        print("AI:")
        for chunk in response:
            if chunk.choices[0].delta.content:
                resp=chunk.choices[0].delta.content
                msg+=resp
                print(resp,end="",flush=True)
        print("\n")
        messages.append({"role":"assistant","content":msg})
