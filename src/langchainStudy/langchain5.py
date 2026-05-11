# from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

embed = OllamaEmbeddings(model="qwen3-embedding",base_url="http://localhost:11434")

res = embed.embed_query("hello world")

res_doc = embed.embed_documents(["hello world","hello python","hello langchain"])
print(res.__len__())

print(len(res))

print(len(res_doc))

print(res_doc[0].__len__())

# print(res_doc)