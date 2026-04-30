from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

response = client.chat.completions.create(
    model="tencent/hy3-preview:free",
    messages=[
        {"role":"system",
         "content":"你是一个专业的Python编程导师，用简洁清晰的方式回答问题，避免冗长。"
        },
        {"role":"user",
         "content":"我是初学者，我该怎么学习python"

        }
    ]
)
print(response.choices[0].message.content)