md5_dir="./md5_db"
md5_path="./md5_db/knowledge_base.text"

# chroma
collection_name="knowledge_base_collection"
chroma_db_path="./chroma_db"
similarity_threshold=2

# spliter
chunk_size=200
chunk_overlap=20
separators=["\n\n","\n", " ", ",", ".", "!", "?", ";", ":",""]
max_split_char_length=100

# model
embedding_model="qwen3-embedding:4b"
chat_model="deepseek-r1:8b"

# chat history
history_storage_path="./chat_history"
session_id="default"
