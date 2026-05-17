import os
import config.config_data as config
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import embeddings
from datetime import datetime
from pathlib import Path
def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):

        os.makedirs(config.md5_dir,exist_ok=True)
        open(config.md5_path,"w",encoding="UTF-8").close()
        return False
    else:
        # for line in open(config.md5_path,"r",encoding="UTF-8").readlines():
        #     line = line.strip()
        #     if line == md5_str:
        #         return True
        with open(config.md5_path,"r",encoding="UTF-8") as f:
            for line in f:
                line = line.strip()
                if line == md5_str:
                    return True
        return False

def save_md5(md5_str: str):
    # open(config.md5_path,"a",encoding="UTF-8").write(md5_str+"\n")
    with open(config.md5_path,"a",encoding="UTF-8") as f:
        f.write(md5_str+"\n")

def get_string_md5(input_string: str,encoding="utf-8"):
    str_bytes = input_string.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

embeddings = embeddings.OllamaEmbeddings(model="qwen3-embedding", base_url="http://localhost:11434")


class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=embeddings,
            persist_directory=config.chroma_db_path
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
            separators=config.separators
        )


    def add_knowledge(self,data: str,filename):
        md5_hex = get_string_md5(data,"utf-8")
        if check_md5(md5_hex):
            # st.warning("该文件已存在！")
            return "该文件已存在！跳过"
        else:
            data_chunks = list([])
            if len(data) > config.max_split_char_length:
                data_chunks = self.splitter.split_text(data)
            else:
                data_chunks.append(data)

            metadata={
                "source": filename,
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator": "RAG_TEST_USER1"
            }

            self.chroma.add_texts(
                data_chunks,
                metadatas = [metadata for _ in data_chunks]
            )

            save_md5(md5_hex)     
            return "添加成功！"

    def get_knowledge(self,query):
        return self.chroma.similarity_search(query,k=2)
    
# if __name__ == "__main__":
#     res = KnowledgeBaseService.get_knowledge("退货率分析")
#     for chunk in res:
#         print(chunk)