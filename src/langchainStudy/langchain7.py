#fewshot prompt template 使用
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM

promptTemplate = PromptTemplate.from_template("单词：{word},词性：{part_of_speach},意思:{meaning},反义词：{antonym},同义词：{synonym}")

example_prompt =[
    {"word": "happy", "part_of_speach": "形容词", "meaning": "快乐的", "antonym": "sad", "synonym": "joyful"},
    {"word": "love", "part_of_speach": "动词", "meaning": "爱", "antonym": "hate", "synonym": "adore"},
    {"word": "big", "part_of_speach": "形容词", "meaning": "大的", "antonym": "small", "synonym": "large"},
    {"word":"neighbor", "part_of_speach": "名词", "meaning": "邻居", "antonym": "non", "synonym": "neighbor"}
]

few_promptTemplate = FewShotPromptTemplate(
    examples=example_prompt,
    example_prompt=promptTemplate,
    prefix="请根据以下单词信息，分析单词的词性、意思、反义词和同义词",
    suffix="基于实例告诉我，{input_word}这个单词的词性、意思、反义词和同义词是什么？",
    input_variables=["input_word"] 
)

model = OllamaLLM(model="qwen2.5:7b",base_url="http://localhost:11434")

def main(inputString):

    chain = few_promptTemplate|model

    res = chain.stream({"input_word": {inputString}})
    for r in res:
        print(r, end="", flush=True)


if __name__ == "__main__":
    while True:
        inputString = input("请输入一个单词：")
        if not inputString:
            print("输入不能为空，请重新输入")
            continue
        if inputString == "q":
            q = input("确定要退出吗？y/n：")
            if q == "y":
                break
            else: 
                continue
        main(inputString)
        print("\n")