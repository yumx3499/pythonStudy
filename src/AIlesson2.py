from openai import OpenAI 

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

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
            model="qwen2.5:7b",
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
main2()