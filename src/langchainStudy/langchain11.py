from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader
import sys

# 使用本地 Ollama 的 qwen3-embedding（确保 Ollama 已安装并运行）
try:
    embedding = OllamaEmbeddings(model="qwen3-embedding", base_url="http://localhost:11434")
except Exception as e:
    print("无法初始化 OllamaEmbeddings。请确保 Ollama 已安装并运行，且已拉取模型 qwen3-embedding (ollama pull qwen3-embedding)。")
    print("错误详情:", e)
    sys.exit(1)

vectorstore = InMemoryVectorStore(embedding=embedding)

loader = CSVLoader(file_path="./testSimpleFile/vectorstoresSimple.csv", 
                   encoding="utf-8")

documents = loader.load()

vectorstore.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1, len(documents)+1)]
)

vectorstore.delete(["id1", "id2"])

results = vectorstore.similarity_search(
    query = "区块链的核心特点是什么？",
    k=2
)

print("similarity_search 返回:")
for r in results:
    print(r)