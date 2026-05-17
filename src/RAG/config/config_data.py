md5_dir="./md5_db"
md5_path="./md5_db/knowledge_base.text"

# chroma
collection_name="knowledge_base_collection"
chroma_db_path="./chroma_db"

# spliter
chunk_size=200
chunk_overlap=20
separators=["\n\n","\n", " ", ",", ".", "!", "?", ";", ":",""]
max_split_char_length=1000